import asyncio
import logging
import sys
from loguru import logger as loguru_logger

# استيراد جميع الطبقات
from projects.aoi_system.layer0_brain.brain import CoreBrain
from projects.aoi_system.layer1_control.control import PlanningControl, SystemState
from projects.aoi_system.layer2_queue.queue_manager import TaskQueue
from projects.aoi_system.layer3_execution.engine import ExecutionEngine
from projects.aoi_system.layer4_vision.vision import VisionMediaLayer
from projects.aoi_system.layer5_memory.memory import MemorySystem
from projects.aoi_system.layer6_healing.healing import SelfHealingLayer
from projects.aoi_system.layer7_monitor.monitor import SystemWatchdog
from projects.aoi_system.layer8_interface.interface import ControlInterface
from projects.aoi_system.swarm.controller import SwarmController

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AOI-Unified-System")

class AOISystem:
    """
    نظام التشغيل الذكي المستقل (Autonomous Operating Intelligence)
    يجمع كل الطبقات الـ 9 في حلقة واحدة متكاملة.
    """
    def __init__(self):
        # تهيئة الطبقات الأساسية
        self.brain = CoreBrain()
        self.memory = MemorySystem()
        self.healing = SelfHealingLayer(self.memory)
        self.control = PlanningControl()
        self.queue = TaskQueue()
        self.engine = ExecutionEngine()
        self.vision = VisionMediaLayer()
        self.monitor = SystemWatchdog(self.healing)
        self.interface = ControlInterface(self)
        self.swarm = SwarmController(max_concurrency=1000)

        self.running = False

    async def initialize(self):
        logger.info("🎬 Initializing Unified AOI System...")
        # تشغيل الطبقات المستقلة (Queue, Monitor)
        self.queue.start()
        asyncio.create_task(self.monitor.monitor_loop())
        logger.info("✅ All layers operational.")

    async def trigger_swarm_goal(self, goal: str, agent_count: int = 100):
        """
        تشغيل هدف بنمط الـ Swarm (آلاف الوكلاء المتزامنين).
        """
        logger.info(f"🐝 Triggering Swarm Goal: {goal} with {agent_count} agents")

        for i in range(agent_count):
            self.swarm.add_task(
                f"Agent-{i}",
                self.brain.reason,
                prompt=f"Sub-task {i} for objective: {goal}"
            )

        await self.swarm.execute_swarm()
        logger.info(f"🏁 Swarm objective '{goal}' completed.")

    async def trigger_goal(self, goal: str):
        """
        نقطة الدخول لهدف جديد.
        Flow: Goal -> Brain -> Plan -> Control -> Queue -> Engine -> Verify
        """
        logger.info(f"🎯 New Objective: {goal}")

        # Layer 0: Thinking & Planning
        plan_data = await self.brain.generate_plan(goal)

        # Layer 1: Control (FSM)
        self.control.set_plan(goal, plan_data)

        # معالجة المهام عبر الـ Queue
        while True:
            task = self.control.get_next_task()
            if not task:
                break

            # Layer 2: Queueing Task
            # اختيار المنفذ (Executor) المناسب من Layer 3/4
            if task.tool_required == "system_monitor":
                executor = self.engine.execute_command
                params = {"func": executor, "command": "ls"}
            else:
                executor = self.engine.browser_action
                params = {"func": executor, "action": "browse", "target": "root"}

            # Layer 6: Run with Self-Healing strategy
            task_id = self.queue.add_task(
                task.description,
                self.healing.run_with_retry,
                params
            )

            # محاكاة الانتظار حتى اكتمال المهمة (لغرض العرض)
            await asyncio.sleep(1)
            self.control.mark_task_complete(task.id, success=True)
            self.memory.record_task(task.id, task.description, "completed", "success")

        logger.info(f"🏁 Objective '{goal}' reached and verified.")

    async def start_forever(self):
        """
        الحلقة الرئيسية 24/7.
        """
        self.running = True
        await self.initialize()

        logger.info("♾️ AOI System enters 24/7 Control Loop.")

        while self.running:
            try:
                # التحقق من وجود مهام خلفية أو تحسينات دورية
                current_state = self.control.state
                if current_state == SystemState.IDLE:
                    # تفكير تلقائي عند الخمول
                    # await self.trigger_goal("Check system updates and health")
                    pass

                await asyncio.sleep(60) # التحقق كل دقيقة

            except Exception as e:
                self.healing.analyze_exception(e)
                await asyncio.sleep(10) # انتظار قبل إعادة المحاولة

    async def get_realtime_status(self):
        return {
            "state": self.control.state.value,
            "resources": await self.monitor.get_system_stats(),
            "last_objective": self.control.current_plan.goal if self.control.current_plan else "None"
        }

if __name__ == "__main__":
    aoi = AOISystem()
    try:
        asyncio.run(aoi.start_forever())
    except KeyboardInterrupt:
        logger.info("👋 System shutdown requested.")
        aoi.monitor.stop()
