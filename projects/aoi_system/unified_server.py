import logging
import asyncio
import os
from pathlib import Path
from fastapi import FastAPI, WebSocket, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# استيراد النظام الموحد
from projects.aoi_system.main_aoi import AOISystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AOI-Unified-Server")

class UnifiedServer:
    """
    السيرفر الموحد (Unified SSOT)
    يجمع بين خدمات الـ AOI والـ AI Agent والـ DeOS في بوابة واحدة.
    """
    def __init__(self):
        self.app = FastAPI(title="AOI Unified Control System")
        self.aoi = AOISystem()
        self._setup_middleware()
        self._setup_routes()
        self._setup_static()

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        @self.app.get("/api/status")
        async def get_status():
            return await self.aoi.get_realtime_status()

        @self.app.post("/api/goal")
        async def trigger_goal(goal: str):
            asyncio.create_task(self.aoi.trigger_goal(goal))
            return {"status": "Executing", "goal": goal}

        @self.app.post("/api/swarm/goal")
        async def trigger_swarm(goal: str, agents: int = 10):
            asyncio.create_task(self.aoi.trigger_swarm_goal(goal, agents))
            return {"status": "Swarm Launched", "agents": agents}

        @self.app.post("/api/schedule")
        async def schedule_task(name: str, request: str, task_type: str, time_iso: str):
            from datetime import datetime
            run_at = datetime.fromisoformat(time_iso)
            job_id = await self.aoi.schedule_new_task(name, request, task_type, run_at)
            return {"status": "Scheduled", "job_id": job_id}

        # دمج مسارات الـ AI Agent القديم
        @self.app.post("/api/predict")
        async def predict_motion(data: dict):
            if self.aoi.predictor:
                self.aoi.predictor.record_motion(tuple(data.get('pos', [0,0])), data.get('ts', 0))
                return self.aoi.predictor.predict_next_position()
            return {"error": "Predictor module not loaded"}

        @self.app.post("/api/gallery/upload")
        async def upload_media(file: UploadFile = File(...)):
            content = await file.read()
            # محاكاة الرفع للمعرض
            return {"status": "Success", "filename": file.filename, "size": len(content)}

        @self.app.websocket("/ws/monitor")
        async def websocket_monitor(websocket: WebSocket):
            await websocket.accept()
            try:
                while True:
                    stats = await self.aoi.get_realtime_status()
                    await websocket.send_json(stats)
                    await asyncio.sleep(2)
            except Exception:
                pass

    def _setup_static(self):
        # توحيد مجلدات الـ Frontend
        frontend_path = Path("projects/ai_agent/frontend")
        if frontend_path.exists():
            self.app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
            logger.info(f"📁 Mounted frontend from {frontend_path}")

    async def start(self):
        await self.aoi.initialize()
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

if __name__ == "__main__":
    server = UnifiedServer()
    asyncio.run(server.start())
