import logging
from fastapi import FastAPI, WebSocket
import uvicorn
from typing import Dict, Any

logger = logging.getLogger("AOI-Layer8-Interface")

class ControlInterface:
    """
    LAYER 8 – Interface & Control
    المسؤولية: التحكم الخارجي، المتابعة
    """
    def __init__(self, main_loop):
        self.app = FastAPI(title="AOI Control Panel")
        self.main_loop = main_loop
        self._setup_routes()
        logger.info("📱 Control Interface Layer (FastAPI) initialized.")

    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"status": "AOI Operational", "current_state": self.main_loop.control.state.value}

        @self.app.get("/stats")
        async def stats():
            return await self.main_loop.monitor.get_system_stats()

        @self.app.post("/goal")
        async def set_goal(goal: str):
            await self.main_loop.trigger_goal(goal)
            return {"message": f"Goal received: {goal}"}

        @self.app.post("/schedule")
        async def schedule_task(name: str, request: str, task_type: str, time_iso: str):
            """
            جدولة مهمة عبر API.
            """
            from datetime import datetime
            run_at = datetime.fromisoformat(time_iso)
            job_id = await self.main_loop.schedule_new_task(name, request, task_type, run_at)
            return {"status": "Scheduled", "job_id": job_id, "run_at": time_iso}

        @self.app.get("/scheduled")
        async def get_scheduled():
            return self.main_loop.scheduler.get_all_jobs()

        @self.app.websocket("/ws/monitor")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                data = await self.main_loop.get_realtime_status()
                await websocket.send_json(data)

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        logger.info(f"🌐 Starting Interface on http://{host}:{port}")
        # uvicorn.run(self.app, host=host, port=port) # سيتم تشغيله بشكل منفصل
