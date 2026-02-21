import asyncio
from typing import Dict, Any
import logging
import time

logger = logging.getLogger("AOI-DePIN-Contribution")

class ContributionManager:
    def __init__(self):
        self.total_credits_earned = 0.0
        self.is_active = False

    async def start_contribution(self, provider: str, user_approved: bool = False) -> Dict[str, Any]:
        if not user_approved:
            return {"success": False, "error": "User approval required"}
        
        self.is_active = True
        logger.info(f"💎 Starting resource contribution to {provider}")
        asyncio.create_task(self._contribution_loop())
        return {"success": True, "session_id": f"s_{int(time.time())}", "estimated_credits": 10.5}

    async def _contribution_loop(self):
        while self.is_active:
            # Simulate credit earning
            self.total_credits_earned += 0.01
            await asyncio.sleep(60)

    async def stop_contribution(self):
        self.is_active = False
        logger.info("🛑 Resource contribution stopped")

    def get_stats(self):
        return {"total_credits_earned": self.total_credits_earned, "is_active": self.is_active}
