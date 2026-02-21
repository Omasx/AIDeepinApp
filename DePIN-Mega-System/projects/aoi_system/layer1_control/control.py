import logging
import asyncio
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("AOI-Layer1-Control")

class SystemState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    AWAITING_APPROVAL = "awaiting_approval"
    SYNCING = "syncing"
    ERROR = "error"

class Task(BaseModel):
    id: str
    description: str
    tool_required: str
    params: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"

class Plan(BaseModel):
    goal: str
    tasks: List[Task]
    current_step: int = 0

class PlanningControl:
    """
    LAYER 1 – State & Planning Control
    المسؤولية: ضبط التفكير، منع القرارات العشوائية، إدارة دورة Plan -> Act -> Verify
    """
    def __init__(self):
        self.state = SystemState.IDLE
        self.current_plan: Optional[Plan] = None
        self.pending_approvals = {}
        logger.info("🎮 Planning Control Layer initialized.")

    async def submit_for_approval(self, task_id: str, results: Dict[str, Any]):
        """
        إرسال النتائج للمستخدم للموافقة عليها قبل الدمج النهائي.
        """
        self.pending_approvals[task_id] = {
            "results": results,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        self.transition_to(SystemState.AWAITING_APPROVAL)
        logger.info(f"⏳ Task {task_id} is awaiting human approval.")

    async def approve_task(self, task_id: str):
        """
        موافقة المستخدم على النتائج وبدء التزامن.
        """
        if task_id in self.pending_approvals:
            self.pending_approvals[task_id]["status"] = "approved"
            self.transition_to(SystemState.SYNCING)
            logger.info(f"✅ Task {task_id} approved. Starting state synchronization...")
            
            # محاكاة وقت المزامنة (2-3 دقائق كما طلب المستخدم)
            await asyncio.sleep(2) # لغرض العرض، نستخدم ثواني
            
            self.transition_to(SystemState.IDLE)
            return True
        return False

    def transition_to(self, new_state: SystemState):
        logger.info(f"🔄 State Transition: {self.state.value} -> {new_state.value}")
        self.state = new_state

    def set_plan(self, goal: str, tasks_data: List[Dict[str, Any]]):
        tasks = [
            Task(
                id=f"T-{i}",
                description=t["task"],
                tool_required=t["required_tool"]
            ) for i, t in enumerate(tasks_data)
        ]
        self.current_plan = Plan(goal=goal, tasks=tasks)
        self.transition_to(SystemState.PLANNING)

    def get_next_task(self) -> Optional[Task]:
        if not self.current_plan:
            return None
        
        if self.current_plan.current_step < len(self.current_plan.tasks):
            task = self.current_plan.tasks[self.current_plan.current_step]
            self.transition_to(SystemState.EXECUTING)
            return task
        
        self.transition_to(SystemState.VERIFYING)
        return None

    def mark_task_complete(self, task_id: str, success: bool):
        if self.current_plan:
            for task in self.current_plan.tasks:
                if task.id == task_id:
                    task.status = "completed" if success else "failed"
                    self.current_plan.current_step += 1
                    break
        
        self.transition_to(SystemState.PLANNING if success else SystemState.ERROR)
