import logging
import asyncio
from typing import List, Dict, Any
from ..swarm.router import APIRouter, APIKey

logger = logging.getLogger("AOI-Layer0-Brain")

class CoreBrain:
    """
    LAYER 0 – Core Brain (تفكير فقط)
    المسؤولية: Reasoning, Planning, Decision output
    """
    def __init__(self, model_name: str = "Llama 3.5"):
        self.model_name = model_name
        # تهيئة الـ Router مع مفتاح تجريبي
        self.router = APIRouter([APIKey("LocalNode", "key_12345")])
        logger.info(f"🧠 Brain Layer initialized with {self.model_name} and Swarm Router")

    async def reason(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        تحليل الموقف وإعطاء قرار (تفكير فقط).
        """
        logger.info(f"🤔 Reasoning on: {prompt[:50]}...")

        # استخدام الـ Swarm Router لتوزيع الحمل
        return await self.router.call_llm(prompt)

    async def generate_plan(self, goal: str, constraints: List[str] = None) -> List[Dict[str, Any]]:
        """
        تحويل الهدف إلى قائمة مهام مجردة.
        """
        logger.info(f"📋 Generating plan for: {goal}")
        # محاكاة خطة عمل
        return [
            {"step": 1, "task": "Analyze environment state", "required_tool": "system_monitor"},
            {"step": 2, "task": "Search for relevant data", "required_tool": "web_browser"},
            {"step": 3, "task": "Process information", "required_tool": "logic_engine"},
            {"step": 4, "task": "Finalize and report", "required_tool": "interface"}
        ]
