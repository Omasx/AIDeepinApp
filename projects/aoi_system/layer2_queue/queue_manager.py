import logging
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, Callable, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("AOI-Layer2-Queue")

class TaskQueue:
    """
    LAYER 2 – Task Queue & Scheduling
    المسؤولية: منع التوقف، منع التنفيذ المباشر، ضمان الاستمرار بعد إعادة التشغيل
    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.pending_tasks = asyncio.Queue()
        self.running = False
        logger.info("📅 Task Queue & Scheduler Layer initialized.")

    def add_task(self, task_description: str, executor: Callable, params: Dict[str, Any] = None) -> str:
        task_id = str(uuid.uuid4())
        logger.info(f"📥 Task queued: {task_id} - {task_description}")
        # وضع المهمة في الانتظار
        self.pending_tasks.put_nowait({
            "id": task_id,
            "description": task_description,
            "executor": executor,
            "params": params or {},
            "queued_at": datetime.now()
        })
        return task_id

    async def worker(self):
        """
        عامل المعالجة التسلسلي للمهام.
        """
        self.running = True
        logger.info("👷 Task Worker started.")
        while self.running:
            task = await self.pending_tasks.get()
            task_id = task["id"]
            logger.info(f"🔨 Executing Task {task_id}: {task['description']}")

            try:
                # التنفيذ الفعلي عبر المحرك (Layer 3)
                result = await task["executor"](**task["params"])
                logger.info(f"✅ Task {task_id} completed successfully.")
            except Exception as e:
                logger.error(f"❌ Task {task_id} failed: {e}")
            finally:
                self.pending_tasks.task_done()

    def start(self):
        self.scheduler.start()
        asyncio.create_task(self.worker())
