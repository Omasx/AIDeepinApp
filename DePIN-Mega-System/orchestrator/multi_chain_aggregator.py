"""
🔗 Multi-Chain Aggregator API - واجهة موحدة لجميع شبكات DePIN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نظام متكامل للاتصال بـ: Akash, Render, Golem, iExec, Bittensor, Petals
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time
from datetime import datetime
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkType(Enum):
    """أنواع الشبكات المدعومة"""
    AKASH = "akash"
    RENDER = "render"
    GOLEM = "golem"
    IEXEC = "iexec"
    BITTENSOR = "bittensor"
    PETALS = "petals"

class TaskType(Enum):
    """أنواع المهام"""
    COMPUTE = "compute"
    GPU_RENDERING = "gpu_rendering"
    AI_INFERENCE = "ai_inference"
    STORAGE = "storage"
    HYBRID = "hybrid"

@dataclass
class NetworkEndpoint:
    """نقطة نهاية الشبكة"""
    network: NetworkType
    url: str
    api_key: Optional[str] = None
    health_status: str = "unknown"
    latency_ms: float = 0.0
    last_check: Optional[datetime] = None
    free_tier_limit: int = 0
    free_tier_used: int = 0
    success_rate: float = 100.0

@dataclass
class ComputeTask:
    """مهمة الحوسبة"""
    task_id: str
    task_type: TaskType
    requirements: Dict[str, Any]
    priority: int = 5
    timeout_seconds: int = 3600
    retry_count: int = 3
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class ExecutionResult:
    """نتيجة التنفيذ"""
    task_id: str
    network: NetworkType
    status: str  # "success", "failed", "timeout"
    output: Optional[Dict] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    cost_usd: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class AkashConnector:
    """موصل شبكة Akash"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.akashnet.net"
        self.api_key = api_key
        self.network_type = NetworkType.AKASH
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/status", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"Akash health check failed: {e}")
            return False, 0.0
    
    async def submit_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة إلى Akash"""
        try:
            payload = {
                "task_id": task.task_id,
                "type": task.task_type.value,
                "requirements": task.requirements,
                "timeout": task.timeout_seconds
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/tasks",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                ) as resp:
                    if resp.status == 201:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Akash task submission failed: {e}")
            return {"error": str(e)}
    
    async def get_task_status(self, task_id: str) -> Dict:
        """الحصول على حالة المهمة"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=5
                ) as resp:
                    return await resp.json()
        except Exception as e:
            logger.error(f"Akash status check failed: {e}")
            return {"error": str(e)}

class RenderConnector:
    """موصل شبكة Render"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.render.com"
        self.api_key = api_key
        self.network_type = NetworkType.RENDER
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"Render health check failed: {e}")
            return False, 0.0
    
    async def submit_gpu_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة GPU إلى Render"""
        try:
            payload = {
                "task_id": task.task_id,
                "gpu_type": task.requirements.get("gpu_type", "RTX3090"),
                "duration_hours": task.requirements.get("duration", 1),
                "script": task.requirements.get("script", "")
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/gpu-tasks",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                ) as resp:
                    if resp.status == 201:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Render task submission failed: {e}")
            return {"error": str(e)}

class GolemConnector:
    """موصل شبكة Golem"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.golem.network"
        self.api_key = api_key
        self.network_type = NetworkType.GOLEM
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/status", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"Golem health check failed: {e}")
            return False, 0.0
    
    async def submit_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة إلى Golem"""
        try:
            payload = {
                "task_id": task.task_id,
                "docker_image": task.requirements.get("docker_image"),
                "command": task.requirements.get("command"),
                "cpu_cores": task.requirements.get("cpu_cores", 4),
                "memory_gb": task.requirements.get("memory_gb", 8)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/tasks",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                ) as resp:
                    if resp.status == 201:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Golem task submission failed: {e}")
            return {"error": str(e)}

class IExecConnector:
    """موصل شبكة iExec"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.iexec.network"
        self.api_key = api_key
        self.network_type = NetworkType.IEXEC
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"iExec health check failed: {e}")
            return False, 0.0
    
    async def submit_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة إلى iExec"""
        try:
            payload = {
                "task_id": task.task_id,
                "app_address": task.requirements.get("app_address"),
                "input_files": task.requirements.get("input_files", []),
                "args": task.requirements.get("args", "")
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/tasks",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                ) as resp:
                    if resp.status == 201:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"iExec task submission failed: {e}")
            return {"error": str(e)}

class BittensorConnector:
    """موصل شبكة Bittensor"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.bittensor.com"
        self.api_key = api_key
        self.network_type = NetworkType.BITTENSOR
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/status", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"Bittensor health check failed: {e}")
            return False, 0.0
    
    async def submit_inference_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة استدلال إلى Bittensor"""
        try:
            payload = {
                "task_id": task.task_id,
                "model": task.requirements.get("model"),
                "prompt": task.requirements.get("prompt"),
                "max_tokens": task.requirements.get("max_tokens", 100)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/inference",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Bittensor task submission failed: {e}")
            return {"error": str(e)}

class PetalsConnector:
    """موصل شبكة Petals"""
    
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.petals.dev"
        self.api_key = api_key
        self.network_type = NetworkType.PETALS
    
    async def health_check(self) -> Tuple[bool, float]:
        """فحص صحة الشبكة"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/status", timeout=5) as resp:
                    latency = (time.time() - start_time) * 1000
                    return resp.status == 200, latency
        except Exception as e:
            logger.error(f"Petals health check failed: {e}")
            return False, 0.0
    
    async def submit_llm_task(self, task: ComputeTask) -> Dict:
        """إرسال مهمة LLM إلى Petals"""
        try:
            payload = {
                "task_id": task.task_id,
                "model": task.requirements.get("model", "meta-llama/Llama-2-70b"),
                "prompt": task.requirements.get("prompt"),
                "max_new_tokens": task.requirements.get("max_tokens", 512)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=60
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Petals task submission failed: {e}")
            return {"error": str(e)}

class MultiChainAggregator:
    """موصل متعدد السلاسل - الواجهة الموحدة"""
    
    def __init__(self):
        self.connectors = {
            NetworkType.AKASH: AkashConnector(),
            NetworkType.RENDER: RenderConnector(),
            NetworkType.GOLEM: GolemConnector(),
            NetworkType.IEXEC: IExecConnector(),
            NetworkType.BITTENSOR: BittensorConnector(),
            NetworkType.PETALS: PetalsConnector(),
        }
        self.network_status: Dict[NetworkType, NetworkEndpoint] = {}
        self.task_history: List[ExecutionResult] = []
    
    async def initialize(self):
        """تهيئة جميع الموصلات"""
        logger.info("🔗 Initializing Multi-Chain Aggregator...")
        
        for network_type, connector in self.connectors.items():
            health, latency = await connector.health_check()
            
            self.network_status[network_type] = NetworkEndpoint(
                network=network_type,
                url=connector.base_url,
                health_status="healthy" if health else "unhealthy",
                latency_ms=latency,
                last_check=datetime.now()
            )
            
            status_emoji = "✅" if health else "❌"
            logger.info(f"{status_emoji} {network_type.value}: {latency:.2f}ms")
    
    async def get_best_network(self, task_type: TaskType) -> Optional[NetworkType]:
        """اختيار أفضل شبكة للمهمة"""
        
        # تصفية الشبكات الصحية
        healthy_networks = [
            (net, status) for net, status in self.network_status.items()
            if status.health_status == "healthy"
        ]
        
        if not healthy_networks:
            logger.warning("⚠️ No healthy networks available!")
            return None
        
        # اختيار حسب نوع المهمة
        if task_type == TaskType.GPU_RENDERING:
            # تفضيل Render و Golem
            for net, status in healthy_networks:
                if net in [NetworkType.RENDER, NetworkType.GOLEM]:
                    return net
        
        elif task_type == TaskType.AI_INFERENCE:
            # تفضيل Bittensor و Petals
            for net, status in healthy_networks:
                if net in [NetworkType.BITTENSOR, NetworkType.PETALS]:
                    return net
        
        elif task_type == TaskType.COMPUTE:
            # تفضيل Akash و iExec
            for net, status in healthy_networks:
                if net in [NetworkType.AKASH, NetworkType.IEXEC]:
                    return net
        
        # اختيار الشبكة ذات أقل زمن استجابة
        best_network = min(healthy_networks, key=lambda x: x[1].latency_ms)
        return best_network[0]
    
    async def submit_task(self, task: ComputeTask) -> ExecutionResult:
        """إرسال مهمة إلى أفضل شبكة"""
        
        best_network = await self.get_best_network(task.task_type)
        
        if not best_network:
            return ExecutionResult(
                task_id=task.task_id,
                network=NetworkType.AKASH,
                status="failed",
                error="No healthy networks available"
            )
        
        logger.info(f"📤 Submitting task {task.task_id} to {best_network.value}")
        
        connector = self.connectors[best_network]
        start_time = time.time()
        
        try:
            if best_network == NetworkType.RENDER:
                result = await connector.submit_gpu_task(task)
            elif best_network == NetworkType.BITTENSOR:
                result = await connector.submit_inference_task(task)
            elif best_network == NetworkType.PETALS:
                result = await connector.submit_llm_task(task)
            else:
                result = await connector.submit_task(task)
            
            execution_time = (time.time() - start_time) * 1000
            
            if "error" in result:
                exec_result = ExecutionResult(
                    task_id=task.task_id,
                    network=best_network,
                    status="failed",
                    error=result["error"],
                    execution_time_ms=execution_time
                )
            else:
                exec_result = ExecutionResult(
                    task_id=task.task_id,
                    network=best_network,
                    status="success",
                    output=result,
                    execution_time_ms=execution_time,
                    cost_usd=0.0  # Free tier
                )
            
            self.task_history.append(exec_result)
            return exec_result
        
        except Exception as e:
            logger.error(f"❌ Task submission failed: {e}")
            return ExecutionResult(
                task_id=task.task_id,
                network=best_network,
                status="failed",
                error=str(e)
            )
    
    async def get_network_status(self) -> Dict:
        """الحصول على حالة جميع الشبكات"""
        return {
            net.value: {
                "status": status.health_status,
                "latency_ms": status.latency_ms,
                "last_check": status.last_check.isoformat() if status.last_check else None
            }
            for net, status in self.network_status.items()
        }
    
    async def get_statistics(self) -> Dict:
        """الحصول على إحصائيات الأداء"""
        total_tasks = len(self.task_history)
        successful_tasks = len([t for t in self.task_history if t.status == "success"])
        failed_tasks = len([t for t in self.task_history if t.status == "failed"])
        
        avg_execution_time = (
            sum(t.execution_time_ms for t in self.task_history) / total_tasks
            if total_tasks > 0 else 0
        )
        
        return {
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "avg_execution_time_ms": avg_execution_time,
            "total_cost_usd": 0.0  # Always free
        }

# مثال على الاستخدام
async def main():
    print("🔗 Multi-Chain Aggregator - مثال على الاستخدام")
    print("=" * 80)
    
    aggregator = MultiChainAggregator()
    await aggregator.initialize()
    
    print("\n📊 حالة الشبكات:")
    status = await aggregator.get_network_status()
    for network, info in status.items():
        print(f"  {network}: {info['status']} ({info['latency_ms']:.2f}ms)")
    
    # إرسال مهام تجريبية
    print("\n📤 إرسال مهام تجريبية:")
    
    tasks = [
        ComputeTask(
            task_id="task-001",
            task_type=TaskType.GPU_RENDERING,
            requirements={"gpu_type": "RTX3090", "duration": 1}
        ),
        ComputeTask(
            task_id="task-002",
            task_type=TaskType.AI_INFERENCE,
            requirements={"model": "gpt-3", "prompt": "Hello"}
        ),
        ComputeTask(
            task_id="task-003",
            task_type=TaskType.COMPUTE,
            requirements={"cpu_cores": 4, "memory_gb": 8}
        ),
    ]
    
    for task in tasks:
        result = await aggregator.submit_task(task)
        print(f"  {result.task_id}: {result.status} on {result.network.value}")
    
    # الإحصائيات
    print("\n📈 الإحصائيات:")
    stats = await aggregator.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
