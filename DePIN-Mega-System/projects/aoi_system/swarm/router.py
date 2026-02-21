import asyncio
import logging
import itertools
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger("AOI-Swarm-Router")

@dataclass
class APIKey:
    provider: str
    key: str
    rate_limit: int = 5  # Requests per second default

class APIRouter:
    """
    1. The Core Engine: Multi-Key Load Balancer
    المسؤولية: توزيع الطلبات على المفاتيح المتاحة لتقليل زمن الانتظار وتجنب الـ Rate Limits.
    """
    def __init__(self, keys: List[APIKey]):
        self.keys = keys
        self.key_cycle = itertools.cycle(keys) if keys else None
        
        # إذا كان هناك مفتاح واحد، نستخدم Semaphore للتحكم في التدفق
        # إذا كان هناك عدة مفاتيح، نوزع الحمل بينهم
        self.semaphore = asyncio.Semaphore(len(keys) * 5 if keys else 1)
        
        logger.info(f"🔌 APIRouter initialized with {len(keys)} keys.")

    async def call_llm(self, prompt: str, model: str = "llama3.5") -> str:
        """
        توزيع الطلب على أفضل مفتاح متاح (Round-Robin).
        """
        async with self.semaphore:
            if not self.keys:
                logger.warning("⚠️ No API keys configured. Using local fallback.")
                return await self._local_fallback(prompt)

            target_key = next(self.key_cycle)
            logger.info(f"📡 Dispatching request to {target_key.provider} via key ending in ...{target_key.key[-4:]}")
            
            # محاكاة زمن استجابة سريع جداً لتقليل الـ Latency
            # في الحقيقة هنا يتم استدعاء OpenAI API أو Groq أو غيره
            await asyncio.sleep(0.1) 
            return f"Response from {target_key.provider} for: {prompt[:20]}..."

    async def _local_fallback(self, prompt: str) -> str:
        # محاكاة استجابة من نموذج محلي (Ollama/llama.cpp)
        await asyncio.sleep(0.5)
        return f"Local Llama Response to: {prompt[:20]}"

    def add_key(self, provider: str, key: str):
        self.keys.append(APIKey(provider, key))
        self.key_cycle = itertools.cycle(self.keys)
        self.semaphore = asyncio.Semaphore(len(self.keys) * 5)
        logger.info(f"➕ New key added. Total keys: {len(self.keys)}")
