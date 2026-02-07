"""
server.py - السيرفر الرئيسي للمنصة
"""

import asyncio
import json
import logging
from aiohttp import web
import aiohttp
from pathlib import Path
from datetime import datetime
from quantum_storage import QuantumFreeStorage
from session_manager import FreeSessionManager

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIDePINServer:
    """السيرفر الرئيسي للمنصة"""
    
    def __init__(self):
        self.storage = QuantumFreeStorage(cache_size_mb=2048)
        self.session_mgr = FreeSessionManager()
        self.active_connections = {}
        self.websockets = set()
        logger.info("✅ تم تهيئة السيرفر الرئيسي")
    
    async def handle_connect(self, request):
        """معالجة طلب الاتصال"""
        try:
            data = await request.json()
            device_id = data.get("device_id")
            
            if not device_id:
                return web.json_response({
                    "success": False,
                    "error": "معرف الجهاز مطلوب"
                }, status=400)
            
            # إنشاء جلسة مجانية
            session = self.session_mgr.create_free_session(device_id)
            
            logger.info(f"✅ اتصال جديد من: {device_id}")
            
            return web.json_response({
                "success": True,
                "session_token": session["token"],
                "message": "مرحباً! اتصالك مجاني 100%",
                "cost": "0 USD",
                "expires_at": session["expires_at"]
            })
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الاتصال: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def handle_sync_keys(self, request):
        """مزامنة مفاتيح AI"""
        try:
            data = await request.json()
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not self.session_mgr.validate_session(token):
                return web.json_response({
                    "success": False,
                    "error": "جلسة غير صالحة"
                }, status=401)
            
            # حفظ المفاتيح
            api_keys = {
                "openai": data.get("openai", ""),
                "anthropic": data.get("anthropic", ""),
                "google": data.get("google", ""),
                "deepseek": data.get("deepseek", "")
            }
            
            # تخزين المفاتيح بشكل آمن
            qhash = self.storage.store(f"api_keys_{token}", api_keys)
            
            logger.info(f"✅ تمت مزامنة المفاتيح: {qhash[:16]}...")
            
            return web.json_response({
                "success": True,
                "message": "تمت المزامنة بنجاح!",
                "hash": qhash
            })
        except Exception as e:
            logger.error(f"❌ خطأ في المزامنة: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def handle_agent_execute(self, request):
        """تنفيذ أمر عبر الوكيل الذكي"""
        try:
            data = await request.json()
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not self.session_mgr.validate_session(token):
                return web.json_response({
                    "success": False,
                    "error": "جلسة غير صالحة"
                }, status=401)
            
            command = data.get("command", "")
            
            # إنشاء معرف المهمة
            task_id = f"task_{datetime.now().timestamp()}"
            
            # تحديث إحصائيات الجلسة
            self.session_mgr.update_session_stats(token, ai_requests=1)
            
            logger.info(f"🤖 تنفيذ أمر: {command[:50]}...")
            
            # محاكاة التنفيذ
            await asyncio.sleep(0.5)
            
            return web.json_response({
                "success": True,
                "task_id": task_id,
                "message": "جاري التنفيذ...",
                "response": f"تم تنفيذ الأمر: {command}"
            })
        except Exception as e:
            logger.error(f"❌ خطأ في تنفيذ الأمر: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def handle_terminal_execute(self, request):
        """تنفيذ أمر في الترمينال"""
        try:
            data = await request.json()
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not self.session_mgr.validate_session(token):
                return web.json_response({
                    "success": False,
                    "error": "جلسة غير صالحة"
                }, status=401)
            
            command = data.get("command", "")
            
            try:
                import subprocess
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = result.stdout if result.returncode == 0 else result.stderr
                
                logger.info(f"💻 تنفيذ أمر: {command}")
                
                return web.json_response({
                    "success": result.returncode == 0,
                    "output": output,
                    "error": result.stderr if result.returncode != 0 else None
                })
            except subprocess.TimeoutExpired:
                return web.json_response({
                    "success": False,
                    "error": "انتهت مهلة الأمر"
                }, status=408)
        except Exception as e:
            logger.error(f"❌ خطأ في الترمينال: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def handle_websocket(self, request):
        """معالجة اتصال WebSocket"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.websockets.add(ws)
        logger.info(f"🔌 اتصال WebSocket جديد")
        
        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        # معالجة الرسائل
                        logger.debug(f"📨 رسالة: {data}")
                    except json.JSONDecodeError:
                        await ws.send_str("خطأ: JSON غير صحيح")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f'WebSocket error: {ws.exception()}')
        finally:
            self.websockets.discard(ws)
            logger.info(f"🔌 إغلاق اتصال WebSocket")
        
        return ws
    
    async def handle_stats(self, request):
        """إحصائيات النظام"""
        try:
            storage_stats = self.storage.get_stats()
            session_stats = self.session_mgr.get_stats()
            
            return web.json_response({
                "server_type": "AI DePIN Cloud Platform",
                "status": "🟢 متصل",
                "storage": storage_stats,
                "sessions": session_stats,
                "total_cost": "0 USD",
                "pricing_model": "100% FREE Forever",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"❌ خطأ في الإحصائيات: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def handle_health(self, request):
        """فحص صحة السيرفر"""
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": "running"
        })
    
    def run(self, host="0.0.0.0", port=8080):
        """تشغيل السيرفر"""
        app = web.Application()
        
        # المسارات
        app.router.add_post("/connect", self.handle_connect)
        app.router.add_post("/api/sync-keys", self.handle_sync_keys)
        app.router.add_post("/api/agent/execute", self.handle_agent_execute)
        app.router.add_post("/api/terminal/execute", self.handle_terminal_execute)
        app.router.add_get("/stats", self.handle_stats)
        app.router.add_get("/health", self.handle_health)
        app.router.add_get("/ws", self.handle_websocket)
        
        # ملفات ثابتة للواجهة
        app.router.add_static('/static', '../frontend')
        
        # CORS
        from aiohttp_cors import setup as cors_setup, ResourceOptions
        cors = cors_setup(app, defaults={
            "*": ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })
        
        # تطبيق CORS على جميع المسارات
        for route in list(app.router.routes()):
            cors.add(route)
        
        logger.info(f"🚀 بدء السيرفر على {host}:{port}")
        web.run_app(app, host=host, port=port)


# ============================================================================
# نقطة الدخول الرئيسية
# ============================================================================

if __name__ == "__main__":
    server = AIDePINServer()
    server.run(host="0.0.0.0", port=8080)
