import logging
import asyncio
import os
from pathlib import Path
from fastapi import FastAPI, WebSocket, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# استيراد النظام الموحد
from projects.aoi_system.main_aoi import AOISystem
from projects.aoi_system.live_agent.live_executor import LiveAgentExecutor
from projects.aoi_system.live_agent.websocket_manager import WebSocketManager
from projects.aoi_system.layer8_interface.adaptive_ui import AdaptiveUIManager

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
        self.ui_manager = AdaptiveUIManager()

        # التنفيذ المباشر (Ultimate Feature)
        self.ws_manager = WebSocketManager()
        self.live_executor = LiveAgentExecutor(self.ws_manager)
        self.live_executor.agi_agent = self.aoi.brain.super_agent

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
            run_at = datetime.fromisoformat(time_iso)
            job_id = await self.aoi.schedule_new_task(name, request, task_type, run_at)
            return {"status": "Scheduled", "job_id": job_id}

        # --- مسارات AGI الجديدة ---
        @self.app.post("/api/agi/execute")
        async def execute_agi_task(goal: str, user_id: str = "default"):
            # التحقق من الأوامر المحظورة (Basic Security)
            restricted = ["rm -rf", "shutdown", "kill"]
            if any(r in goal.lower() for r in restricted):
                return {"status": "Rejected", "reason": "Restricted command detected"}

            asyncio.create_task(self.aoi.brain.super_agent.execute_complex_task(goal, {"user_id": user_id}))
            return {"status": "AGI Task Started", "goal": goal, "timestamp": str(datetime.now())}

        @self.app.post("/api/maintenance/auto")
        async def run_maintenance(action: str = "full"):
            result = await self.aoi.healing.maintenance.auto_optimize_performance()
            return {"status": "Maintenance performed", "result": result}

        @self.app.post("/api/quantum/storage")
        async def quantum_storage(size_gb: float = 100):
            return await self.aoi.quantum_cloud.allocate_infinite_storage(size_gb)

        @self.app.post("/api/capabilities/video-montage")
        async def video_montage(req: dict):
            return await self.aoi.expanded_capabilities.execute_video_montage_full(req)

        # --- مسارات التطور النهائي V2 ---
        @self.app.post("/api/v2/llama/init")
        async def init_llama_cloud(data: dict):
            return await self.aoi.llama_cloud.initialize_on_login(data)

        @self.app.post("/api/v2/social/post")
        async def create_social_post(content: str, user_did: str, p_type: str = "post"):
            return await self.aoi.social.create_post(user_did, content, p_type)

        @self.app.get("/api/v2/social/feed")
        async def get_social_feed(user_did: str):
            return await self.aoi.social.get_feed(user_did)

        @self.app.post("/api/v2/blockchain/switch")
        async def switch_blockchain(network: str):
            return await self.aoi.blockchain.switch_network(network)

        # --- مسارات DeepSeek-R1 و Supreme Commander ---
        @self.app.get("/api/v2/supreme/status")
        async def get_supreme_status():
            return self.aoi.brain.supreme_commander.get_cluster_status()

        @self.app.post("/api/v2/supreme/execute")
        async def execute_supreme_goal(goal: str):
            # تشغيل في الخلفية لتجنب الـ Timeout
            asyncio.create_task(self.aoi.brain.supreme_commander.execute_supreme_goal(goal))
            return {"status": "Supreme Command Issued", "goal": goal}

        # --- مسارات المتجر العالمي ووكيل الـ GUI ---
        @self.app.get("/api/store/list")
        async def list_stores():
            return self.aoi.store.list_all_stores()

        @self.app.post("/api/store/install")
        async def install_app(name: str, store: str, platform: str):
            return await self.aoi.app_bridge.install_app(name, store, platform)

        @self.app.post("/api/app/launch")
        async def launch_app(app_id: str):
            return await self.aoi.app_bridge.launch_app(app_id)

        @self.app.post("/api/app/mission")
        async def start_gui_mission(app_id: str, mission: str):
            # تشغيل المهمة في الخلفية
            asyncio.create_task(self.aoi.gui_agent.execute_gui_mission(app_id, mission))
            return {"status": "Mission Started", "app_id": app_id}

        @self.app.post("/api/app/approve")
        async def approve_mission_results(task_id: str):
            return await self.aoi.control.approve_task(task_id)

        # --- مسارات الواجهة التكيفية (Adaptive UI) ---
        @self.app.get("/api/ui/layout")
        async def get_ui_layout():
            return self.ui_manager.get_mode_layout_specs()

        @self.app.post("/api/ui/route")
        async def route_ui(task_type: str, app_name: str = None):
            app_info = {"name": app_name, "category": "Gaming"} if "game" in task_type else {}
            return await self.ui_manager.route_ui_by_task(task_type, app_info)

        @self.app.post("/api/ui/switch")
        async def switch_ui_mode(mode: str):
            success = self.ui_manager.set_custom_mode(mode)
            return {"success": success, "new_mode": self.ui_manager.current_mode.value}

        # --- مسارات الميزات الضخمة (Mega Features) ---
        @self.app.post("/api/cloud/init")
        async def init_cloud_brain(user_id: str = "default_user"):
            return await self.aoi.zero_cpu.initialize_cloud_brain()

        @self.app.post("/api/gaming/launch")
        async def launch_cloud_game(game: str, resolution: str = "1080p"):
            return await self.aoi.cloud_gaming.launch_game(game, {"resolution": resolution})

        @self.app.post("/api/creative/launch")
        async def launch_creative_app(app: str):
            return await self.aoi.creative_suite.launch_app(app)

        @self.app.post("/api/automation/workflow")
        async def create_workflow(w_type: str, config: dict):
            if w_type == "content":
                return await self.aoi.automation.create_content_manager_workflow(config)
            return {"error": "Unknown workflow type"}

        @self.app.post("/api/virtualization/run")
        async def run_universal_app(app: str, platform: str):
            if platform == "ios": return await self.aoi.app_runner.run_ios_app(app)
            if platform == "windows": return await self.aoi.app_runner.run_windows_app(app)
            return {"error": "Unsupported platform"}

        @self.app.post("/api/quantum/enhance")
        async def quantum_enhance(img_path: str, e_type: str = "super_resolution"):
            return await self.aoi.quantum_ai.enhance_image_quantum(img_path, e_type)

        @self.app.post("/api/neural/connect")
        async def connect_neural(device: str = "emotiv"):
            return await self.aoi.neural.connect_device(device)

        # --- مسارات الشات بوت والبحث والأمن ---
        @self.app.post("/api/chat")
        async def chat_interaction(message: str, user_id: str = "default_user"):
            return await self.aoi.chatbot.chat(message, user_id)

        @self.app.post("/api/chat/agent/activate")
        async def activate_chat_agent(approved: bool, user_id: str = "default_user"):
            return await self.aoi.chatbot.activate_agent_mode(approved, user_id)

        @self.app.post("/api/research/hyper")
        async def hyper_research(query: str, depth: str = "deep", agents: int = 1000):
            return await self.aoi.researcher.hyper_search(query, depth, agents)

        @self.app.post("/api/security/scan")
        async def security_scan(target: str, approved: bool = False):
            return await self.aoi.hacker.execute_security_scan(target, user_approved=approved)

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
