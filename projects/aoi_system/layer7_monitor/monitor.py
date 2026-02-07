import logging
import psutil
import asyncio
from typing import Dict, List

logger = logging.getLogger("AOI-Layer7-Monitor")

class SystemWatchdog:
    """
    LAYER 7 – System Monitor & Watchdog
    المسؤولية: الاستقرار، الأداء، مراقبة الموارد
    """
    def __init__(self, healing_layer):
        self.healer = healing_layer
        self.monitoring = False
        logger.info("🛡️ System Monitor & Watchdog Layer initialized.")

    async def get_system_stats(self) -> Dict[str, float]:
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent
        }

    async def monitor_loop(self):
        """
        حلقة المراقبة الدائمة.
        """
        self.monitoring = True
        logger.info("📡 System monitoring loop started.")
        while self.monitoring:
            stats = await self.get_system_stats()

            # كشف البطء أو الاستهلاك العالي
            if stats["cpu"] > 90:
                logger.warning("🔥 Critical: High CPU usage detected!")
                # طلب إجراء تعافي
                await self.healer.reboot_module("BackgroundProcesses")

            if stats["ram"] > 90:
                logger.error("🛑 Critical: RAM Exhausted!")
                # إجراءات طارئة لتفريغ الذاكرة

            await asyncio.sleep(10) # فحص كل 10 ثواني

    def stop(self):
        self.monitoring = False
