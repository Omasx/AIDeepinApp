# ipc_api.py - الجسر البرمجي للتحكم في Phantom Grid
import logging
from typing import Dict, Any
from projects.phantom_grid.core.scavenger import ScavengerEngine
from projects.phantom_grid.ai.hive_mind import HiveMindAI
from projects.phantom_grid.storage.rclone_aggregator import RcloneAggregator
from projects.phantom_grid.core.power_manager import PowerAwareManager

logger = logging.getLogger("Phantom-Bridge")

class PhantomBridge:
    """الجسر الذي يسمح لنظام AOI بالتحكم في Phantom Grid"""
    def __init__(self):
        self.scavenger = ScavengerEngine()
        self.hive = HiveMindAI(self.scavenger)
        self.storage = RcloneAggregator()
        self.power = PowerAwareManager()

    async def initialize_all(self):
        """تهيئة كل مكونات Phantom Grid"""
        logger.info("🌉 تهيئة جسر Phantom Grid v4.0...")
        await self.scavenger.start_discovery()
        self.storage.add_remote("phantom_vault", "union", "secure_token")
        return {"status": "Phantom Grid v4.0 Online"}

    async def execute_phantom_command(self, command: str, params: Dict = None) -> Dict[str, Any]:
        """تنفيذ أمر من نظام AOI"""
        logger.info(f"📥 استقبال أمر Phantom: {command}")

        if command == "discover":
            await self.scavenger.start_discovery()
            return await self.scavenger.link_resources()

        elif command == "compute_offload":
            if self.power.can_run_heavy_tasks():
                return await self.hive.distribute_compute(params or {})
            else:
                return {"status": "Rejected", "reason": "Power Constraints"}

        elif command == "get_storage":
            return self.storage.create_union_mount()

        return {"error": "Unknown Command"}

if __name__ == "__main__":
    import asyncio
    async def test():
        bridge = PhantomBridge()
        await bridge.initialize_all()
        res = await bridge.execute_phantom_command("compute_offload", {"data": "test"})
        print(f"Bridge Command Result: {res}")

    asyncio.run(test())
