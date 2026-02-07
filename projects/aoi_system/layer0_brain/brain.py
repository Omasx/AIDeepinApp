import logging
import asyncio
from typing import List, Dict, Any

logger = logging.getLogger("AOI-Layer0-Brain")

class CoreBrain:
    """
    LAYER 0 – Core Brain (تفكير فقط)
    المسؤولية: Reasoning, Planning, Decision output
    """
    def __init__(self, model_name: str = "Llama 3.5"):
        self.model_name = model_name
        logger.info(f"🧠 Brain Layer initialized with {self.model_name}")

    async def reason(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        تحليل الموقف وإعطاء قرار (تفكير فقط).
        """
        logger.info(f"🤔 Reasoning on: {prompt[:50]}...")

        # محاولة الاتصال بـ Ollama محلياً (Standard API)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:11434/api/generate", json={
                    "model": "llama3.5",
                    "prompt": prompt,
                    "stream": False
                }) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "No response from model.")
        except Exception as e:
            logger.warning(f"⚠️ Ollama connection failed, falling back to mock: {e}")

        # محاكاة رد النموذج في حال غياب Ollama
        await asyncio.sleep(1)
        return f"Decision based on {self.model_name}: Goal identified as feasible. Procedure: Systematic execution."

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
