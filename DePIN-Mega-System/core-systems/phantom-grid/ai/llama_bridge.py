#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🧠 LLAMA BRIDGE v2.0                                       ║
║                                                                                ║
║           "جسر الذكاء - Local AI + Cloud Offloading"                          ║
║                                                                                ║
║  Features:                                                                     ║
║  - llama.cpp Integration (Local LLM Inference)                                ║
║  - Cloud Offloading (When local insufficient)                                 ║
║  - Hybrid Execution (Local + Cloud combined)                                  ║
║  - Battery-Aware (Reduce usage on low battery)                                ║
║  - Model Quantization (Q4, Q5, Q8 support)                                    ║
║  - Multi-Model Support (Llama, DeepSeek, Mistral)                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import subprocess
import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configuration for a language model"""
    name: str
    path: str
    context_size: int
    quantization: str  # Q4_K_M, Q5_K_M, Q8_0
    gpu_layers: int
    max_tokens: int


@dataclass
class InferenceTask:
    """An inference task"""
    task_id: str
    prompt: str
    model: str
    max_tokens: int
    temperature: float
    stream: bool = False
    use_cloud: bool = False


class LlamaBridge:
    """
    Llama Bridge - Local AI inference with cloud offloading.
    
    Optimized for Android/Termux:
    - Uses quantized models for memory efficiency
    - Offloads to cloud when context is large
    - Battery-aware throttling
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        self.config = phantom.config['ai']
        
        # Model registry
        self.models: Dict[str, ModelConfig] = {}
        
        # llama.cpp process
        self.llama_process = None
        self.llama_server_url = "http://localhost:8080"
        
        # Cloud endpoints
        self.cloud_endpoints = {
            'deepseek': 'https://api.deepseek.ai/v1/chat/completions',
            'together': 'https://api.together.xyz/v1/chat/completions',
            'groq': 'https://api.groq.com/openai/v1/chat/completions',
        }
        
        # Inference queue
        self.inference_queue: List[InferenceTask] = []
        
        # Stats
        self.stats = {
            'local_inferences': 0,
            'cloud_inferences': 0,
            'tokens_generated': 0,
        }
        
        print("🧠 Llama Bridge initialized")
    
    async def initialize(self):
        """Initialize Llama Bridge"""
        # Register models
        await self._register_models()
        
        # Start llama.cpp server if available
        await self._start_llama_server()
        
        print("✅ Llama Bridge ready")
    
    async def _register_models(self):
        """Register available models"""
        models_dir = './models'
        
        # Default model configurations
        default_models = {
            'llama-2-7b': ModelConfig(
                name='llama-2-7b',
                path=f'{models_dir}/llama-2-7b-chat.Q4_K_M.gguf',
                context_size=4096,
                quantization='Q4_K_M',
                gpu_layers=0,  # CPU only for battery
                max_tokens=2048,
            ),
            'deepseek-1.5b': ModelConfig(
                name='deepseek-1.5b',
                path=f'{models_dir}/deepseek-coder-1.3b-base.Q4_K_M.gguf',
                context_size=16384,
                quantization='Q4_K_M',
                gpu_layers=0,
                max_tokens=4096,
            ),
            'mistral-7b': ModelConfig(
                name='mistral-7b',
                path=f'{models_dir}/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
                context_size=8192,
                quantization='Q4_K_M',
                gpu_layers=0,
                max_tokens=4096,
            ),
        }
        
        # Check which models exist
        for name, config in default_models.items():
            if os.path.exists(config.path):
                self.models[name] = config
                print(f"📦 Model registered: {name}")
    
    async def _start_llama_server(self):
        """Start llama.cpp server"""
        try:
            # Check if llama-server exists
            result = subprocess.run(
                ['which', 'llama-server'],
                capture_output=True
            )
            
            if result.returncode != 0:
                print("⚠️ llama-server not found, local inference disabled")
                return
            
            # Get first available model
            if not self.models:
                print("⚠️ No models available")
                return
            
            model = list(self.models.values())[0]
            
            # Start server
            self.llama_process = subprocess.Popen(
                [
                    'llama-server',
                    '-m', model.path,
                    '-c', str(model.context_size),
                    '-ngl', str(model.gpu_layers),
                    '--host', '127.0.0.1',
                    '--port', '8080',
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            
            # Wait for server to start
            await asyncio.sleep(2)
            
            print(f"🚀 llama.cpp server started with {model.name}")
            
        except Exception as e:
            print(f"llama-server start error: {e}")
    
    async def execute(self, task, node=None) -> Dict[str, Any]:
        """Execute an AI inference task"""
        try:
            payload = task.payload
            
            inference_task = InferenceTask(
                task_id=task.task_id,
                prompt=payload.get('prompt', ''),
                model=payload.get('model', 'llama-2-7b'),
                max_tokens=payload.get('max_tokens', 512),
                temperature=payload.get('temperature', 0.7),
                stream=payload.get('stream', False),
            )
            
            # Decide: local or cloud
            use_cloud = await self._should_use_cloud(inference_task)
            
            if use_cloud:
                return await self._cloud_inference(inference_task)
            else:
                return await self._local_inference(inference_task)
            
        except Exception as e:
            print(f"AI execution error: {e}")
            return {'error': str(e)}
    
    async def _should_use_cloud(self, task: InferenceTask) -> bool:
        """Decide whether to use cloud inference"""
        # Use cloud if:
        
        # 1. Context is large
        if len(task.prompt) > self.config['llama_cpp'].get('cloud_threshold', 2048):
            return True
        
        # 2. Battery is low
        if self.phantom.battery_level < 30 and not self.phantom.is_charging:
            return True
        
        # 3. Local server not available
        if not self.llama_process:
            return True
        
        # 4. Model not available locally
        if task.model not in self.models:
            return True
        
        return False
    
    async def _local_inference(self, task: InferenceTask) -> Dict[str, Any]:
        """Run inference locally with llama.cpp"""
        try:
            print(f"🧠 Local inference: {task.task_id}")
            
            # Use llama.cpp server API
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.llama_server_url}/completion",
                    json={
                        'prompt': task.prompt,
                        'n_predict': task.max_tokens,
                        'temperature': task.temperature,
                        'stream': False,
                    },
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        
                        self.stats['local_inferences'] += 1
                        self.stats['tokens_generated'] += result.get('tokens_evaluated', 0)
                        
                        return {
                            'status': 'success',
                            'source': 'local',
                            'model': task.model,
                            'content': result.get('content', ''),
                            'tokens': result.get('tokens_evaluated', 0),
                        }
                    else:
                        # Fallback to cloud
                        return await self._cloud_inference(task)
            
        except Exception as e:
            print(f"Local inference error: {e}")
            # Fallback to cloud
            return await self._cloud_inference(task)
    
    async def _cloud_inference(self, task: InferenceTask) -> Dict[str, Any]:
        """Run inference on cloud API"""
        try:
            print(f"☁️ Cloud inference: {task.task_id}")
            
            # Select endpoint
            endpoint = self.cloud_endpoints.get('deepseek')
            
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    headers={
                        'Authorization': f"Bearer {os.environ.get('DEEPSEEK_API_KEY', '')}",
                        'Content-Type': 'application/json',
                    },
                    json={
                        'model': 'deepseek-chat',
                        'messages': [
                            {'role': 'user', 'content': task.prompt}
                        ],
                        'max_tokens': task.max_tokens,
                        'temperature': task.temperature,
                    },
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        
                        self.stats['cloud_inferences'] += 1
                        self.stats['tokens_generated'] += result.get('usage', {}).get('total_tokens', 0)
                        
                        return {
                            'status': 'success',
                            'source': 'cloud',
                            'model': 'deepseek-chat',
                            'content': result['choices'][0]['message']['content'],
                            'tokens': result.get('usage', {}).get('total_tokens', 0),
                        }
                    else:
                        error_text = await resp.text()
                        return {
                            'status': 'error',
                            'error': f"Cloud API error: {resp.status} - {error_text}",
                        }
            
        except Exception as e:
            print(f"Cloud inference error: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def stream_inference(self, task: InferenceTask) -> AsyncGenerator[str, None]:
        """Stream inference results"""
        # Implementation for streaming
        yield "Streaming not implemented in this version"
    
    async def load_model(self, model_name: str) -> bool:
        """Load a specific model"""
        if model_name not in self.models:
            print(f"❌ Model not found: {model_name}")
            return False
        
        # Restart server with new model
        if self.llama_process:
            self.llama_process.terminate()
            await asyncio.sleep(1)
        
        await self._start_llama_server()
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get AI inference statistics"""
        return {
            'models': list(self.models.keys()),
            'local_inferences': self.stats['local_inferences'],
            'cloud_inferences': self.stats['cloud_inferences'],
            'tokens_generated': self.stats['tokens_generated'],
        }
    
    async def close(self):
        """Close Llama Bridge"""
        if self.llama_process:
            self.llama_process.terminate()
            print("🔒 Llama Bridge closed")
