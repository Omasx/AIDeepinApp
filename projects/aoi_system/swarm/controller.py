import asyncio
import logging
from typing import List, Dict, Any, Callable, Coroutine
from dataclasses import dataclass, field

logger = logging.getLogger("AOI-Swarm-Controller")

@dataclass
class SwarmTask:
    id: str
    coro_func: Callable[..., Coroutine]
    args: tuple = ()
    kwargs: Dict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    completed: asyncio.Event = field(default_factory=asyncio.Event)

class SwarmController:
    """
    2. The Swarm Architecture (10,000+ Agents)
    المسؤولية: إدارة آلاف المهام المتزامنة بكفاءة عالية باستخدام asyncio و DAG.
    """
    def __init__(self, max_concurrency: int = 1000):
        self.tasks: Dict[str, SwarmTask] = {}
        self.semaphore = asyncio.Semaphore(max_concurrency)
        logger.info(f"🐝 Swarm Controller ready. Max Concurrency: {max_concurrency}")

    def add_task(self, task_id: str, coro_func: Callable, dependencies: List[str] = None, *args, **kwargs):
        self.tasks[task_id] = SwarmTask(
            id=task_id,
            coro_func=coro_func,
            args=args,
            kwargs=kwargs,
            dependencies=dependencies or []
        )
        logger.debug(f"📝 Task added to swarm: {task_id}")

    async def _execute_task(self, task: SwarmTask):
        # 1. انتظر انتهاء المهام المعتمد عليها (DAG dependency management)
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                await self.tasks[dep_id].completed.wait()

        # 2. حجز مكان في الـ Concurrency Pool
        async with self.semaphore:
            try:
                logger.debug(f"🚀 Running Swarm Worker: {task.id}")
                task.result = await task.coro_func(*task.args, **task.kwargs)
            except Exception as e:
                logger.error(f"❌ Swarm Task {task.id} failed: {e}")
            finally:
                task.completed.set()

    async def execute_swarm(self):
        """
        تشغيل جميع المهام المضافة بأقصى سرعة ممكنة مع احترام التبعيات.
        """
        logger.info(f"🔥 Launching Swarm Execution for {len(self.tasks)} tasks...")
        start_time = asyncio.get_event_loop().time()

        # إنشاء جميع المهام كـ coroutines وتشغيلها بشكل متزامن
        await asyncio.gather(*(self._execute_task(t) for t in self.tasks.values()))

        end_time = asyncio.get_event_loop().time()
        logger.info(f"🏁 Swarm completed in {end_time - start_time:.2f}s")

    def get_results(self) -> Dict[str, Any]:
        return {tid: t.result for tid, t in self.tasks.items()}
