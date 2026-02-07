import asyncio
import logging
import time
from typing import Optional
from .orchestrator import LlamaOrchestrator
from .monitor import SystemMonitor
from .memory import LongTermMemory
from .self_healing import SelfHealer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DeOS-Kernel")

class DeOSKernel:
    """
    نواة نظام DeOS - تدير الحلقة اللانهائية للتشغيل الذاتي.
    """
    def __init__(self):
        self.orchestrator = LlamaOrchestrator()
        self.monitor = SystemMonitor()
        self.memory = LongTermMemory()
        self.healer = SelfHealer(self.monitor)
        self.is_running = False

    async def start_loop(self):
        """
        تشغيل النظام 24/7.
        """
        self.is_running = True
        logger.info("🚀 DeOS Kernel started. Operating autonomously...")

        while self.is_running:
            try:
                # 1. مراقبة النظام
                health_report = await self.monitor.check_status()
                logger.info(f"📊 Health Check: {health_report}")

                # 2. فحص الذاكرة عن مهام معلقة أو أهداف طويلة الأمد
                current_goal = self.memory.get_active_goal()

                if not current_goal:
                    # إذا لم يكن هناك هدف، ابحث عن فرص للتحسين الذاتي
                    current_goal = "Optimizing system performance and scanning for updates."

                logger.info(f"🎯 Current Goal: {current_goal}")

                # 3. التخطيط والتنفيذ عبر الأوركستراتور (Llama 3.5)
                plan = await self.orchestrator.create_plan(current_goal, health_report)
                for task in plan:
                    result = await self.orchestrator.execute_task(task)
                    self.memory.record_execution(task, result)

                # 4. الإصلاح التلقائي إذا لزم الأمر
                if not health_report["healthy"]:
                    await self.healer.repair_system(health_report["issues"])

                # 5. التقييم والتعلم
                await self.memory.evaluate_performance()

                # انتظار قصير قبل الدورة القادمة
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"⚠️ Kernel Error: {e}")
                await asyncio.sleep(10) # إعادة محاولة بعد خطأ

    def stop(self):
        self.is_running = False
        logger.info("🛑 DeOS Kernel shutting down.")

if __name__ == "__main__":
    kernel = DeOSKernel()
    asyncio.run(kernel.start_loop())
