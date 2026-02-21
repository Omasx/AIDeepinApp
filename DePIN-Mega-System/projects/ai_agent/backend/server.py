# server.py - السيرفر الرئيسي مع نقاط API المتقدمة
import asyncio
import logging
from aiohttp import web
import json
from datetime import datetime
from pathlib import Path
import os
import aiohttp_cors

# استيراد المكونات - مسارات موحدة
try:
    from projects.ai_agent.backend.advanced_agent.autonomous_agent import AutonomousAgent
    from projects.ai_agent.backend.depin_network.quantum_optimizer import QuantumOptimizer
    from projects.ai_agent.backend.depin_network.spacetime_optimizer import SpacetimeOptimizer
except ImportError:
    from advanced_agent.autonomous_agent import AutonomousAgent
    from depin_network.quantum_optimizer import QuantumOptimizer
    from depin_network.spacetime_optimizer import SpacetimeOptimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIDePINServerAdvanced:
    def __init__(self):
        self.autonomous_agent = None
        self.active_websockets = set()
        
    async def initialize(self):
        logger.info("🚀 تهيئة السيرفر المتقدم...")
        api_keys = {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'anthropic': os.getenv('ANTHROPIC_API_KEY', ''),
            'google': os.getenv('GOOGLE_API_KEY', ''),
            'deepseek': os.getenv('DEEPSEEK_API_KEY', ''),
            'github': os.getenv('GITHUB_TOKEN', '')
        }
        self.autonomous_agent = AutonomousAgent(api_keys, '/tmp/agent_storage')
        await self.autonomous_agent.initialize()
        logger.info("✅ السيرفر جاهز!")

    async def handle_agent_execute(self, request):
        data = await request.json()
        user_id = data.get('user_id', 'default')
        command = data.get('command')
        if not command:
            return web.json_response({"success": False, "error": "Command missing"}, status=400)
        result = await self.autonomous_agent.execute_command(command, user_id)
        return web.json_response(result)

    async def handle_get_projects(self, request):
        projects = self.autonomous_agent.get_all_projects()
        return web.json_response(projects)

    async def handle_sync_keys(self, request):
        data = await request.json()
        self.autonomous_agent.api_keys.update(data)
        await self.autonomous_agent.multi_ai_coordinator.sync_all_models()
        return web.json_response({"success": True, "message": "Keys synced"})

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.active_websockets.add(ws)
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    if msg.data == 'ping': await ws.send_str('pong')
        finally:
            self.active_websockets.remove(ws)
        return ws

    def run(self, host="0.0.0.0", port=8000):
        app = web.Application()
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*"
            )
        })
        
        # Get absolute path to frontend directory
        base_dir = Path(__file__).parent.parent
        frontend_dir = base_dir / "frontend"
        
        routes = [
            web.post('/api/agent/execute', self.handle_agent_execute),
            web.get('/api/agent/projects', self.handle_get_projects),
            web.post('/api/agent/sync-keys', self.handle_sync_keys),
            web.get('/ws/agent', self.handle_websocket),
            web.static('/static', str(frontend_dir)),
            web.get('/', lambda r: web.FileResponse(str(frontend_dir / "agent_panel.html")))
        ]
        
        for route in routes:
            if hasattr(route, 'method'): # Standard route
                cors.add(app.router.add_route(route.method, route.path, route.handler))
            else: # Static route
                app.router.add_routes([route])

        async def on_startup(app):
            await self.initialize()
        app.on_startup.append(on_startup)
        
        web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    server = AIDePINServerAdvanced()
    server.run()
