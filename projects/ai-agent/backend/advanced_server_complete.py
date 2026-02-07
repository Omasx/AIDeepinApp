# advanced_server_complete.py - السيرفر النهائي الكامل المتكامل
from aiohttp import web
import aiohttp_cors
import asyncio
import logging
from pathlib import Path
import os

# استيراد جميع المكونات المتقدمة
from advanced_agent.autonomous_agent import AutonomousAgent
from quantum_prediction.motion_predictor import QuantumMotionPredictor
from universal_platform.platform_manager import UniversalPlatformManager
from media_gallery.gallery_manager import MediaGalleryManager
from auto_scaling.scaling_manager import AutoScalingManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteAIDePINServer:
    def __init__(self):
        self.agent = None
        self.predictor = QuantumMotionPredictor()
        self.platform = UniversalPlatformManager()
        self.gallery = MediaGalleryManager()
        self.scaler = AutoScalingManager()

    async def initialize(self):
        logger.info("🚀 تهيئة النظام السحابي الكامل...")
        api_keys = {'openai': os.getenv('OPENAI_API_KEY', '')}
        self.agent = AutonomousAgent(api_keys, '/tmp/agent_storage')
        await self.agent.initialize()
        asyncio.create_task(self.scaler.start_monitoring())
        logger.info("✅ جميع الأنظمة السحابية جاهزة (مجانية 100%)")

    async def handle_predict_motion(self, request):
        data = await request.json()
        self.predictor.record_motion(tuple(data.get('pos', [0,0])), data.get('ts', 0))
        result = self.predictor.predict_next_position()
        return web.json_response(result)

    async def handle_gallery_upload(self, request):
        data = await request.post()
        content = await data['file'].read()
        result = await self.gallery.upload_media(content, data['file'].filename)
        return web.json_response(result)

    def run(self, host="0.0.0.0", port=8080):
        app = web.Application()
        cors = aiohttp_cors.setup(app, defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*")})

        base_dir = Path(__file__).parent.parent
        frontend_dir = base_dir / "frontend"

        routes = [
            web.post('/api/predict', self.handle_predict_motion),
            web.post('/api/gallery/upload', self.handle_gallery_upload),
            web.static('/static', str(frontend_dir))
        ]

        for route in routes:
            if hasattr(route, 'method'): cors.add(app.router.add_route(route.method, route.path, route.handler))
            else: app.router.add_routes([route])

        async def on_startup(app): await self.initialize()
        app.on_startup.append(on_startup)
        web.run_app(app, host=host, port=port)

if __name__ == "__main__":
    server = CompleteAIDePINServer()
    server.run()
