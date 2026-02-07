import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Callable, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger("AOI-Layer2-Scheduler")

class AOIScheduler:
    """
    LAYER 2 – Scheduling & Timing
    المسؤولية: إدارة المهام المجدولة، التوقيت، والتنفيذ المتزامن للمهام الموقوتة.
    """
    def __init__(self, task_queue):
        self.scheduler = AsyncIOScheduler()
        self.task_queue = task_queue
        logger.info("⏰ AOI Scheduler initialized.")

    def schedule_task(self, name: str, request: str, task_type: str, run_at: datetime, executor: Callable, params: Dict[str, Any] = None):
        """
        جدولة مهمة في وقت محدد.
        """
        job_id = f"job_{uuid.uuid4().hex[:8]}"

        # دالة وسيطة لإضافة المهمة للطابور عند حلول الوقت
        async def job_wrapper():
            logger.info(f"🔔 Scheduled task triggered: {name}")
            self.task_queue.add_task(f"Scheduled: {name} - {request}", executor, params)

        self.scheduler.add_job(
            job_wrapper,
            trigger=DateTrigger(run_date=run_at),
            id=job_id,
            name=name
        )

        logger.info(f"📅 Task '{name}' scheduled for {run_at.isoformat()}")
        return job_id

    def schedule_cron(self, name: str, request: str, cron_expr: str, executor: Callable, params: Dict[str, Any] = None):
        """
        جدولة مهمة دورية (Cron).
        """
        job_id = f"cron_{uuid.uuid4().hex[:8]}"

        async def job_wrapper():
            logger.info(f"🔁 Recurring task triggered: {name}")
            self.task_queue.add_task(f"Recurring: {name} - {request}", executor, params)

        self.scheduler.add_job(
            job_wrapper,
            trigger=CronTrigger.from_crontab(cron_expr),
            id=job_id,
            name=name
        )
        logger.info(f"🗓️ Recurring task '{name}' scheduled with cron: {cron_expr}")
        return job_id

    def get_all_jobs(self):
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            } for job in self.scheduler.get_jobs()
        ]

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("🚀 AOI Scheduler started.")

    def stop(self):
        self.scheduler.shutdown()
        logger.info("🛑 AOI Scheduler stopped.")
