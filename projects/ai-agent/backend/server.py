# server.py - السيرفر الرئيسي مع نقاط API المتقدمة
import asyncio
import logging
from aiohttp import web
import json
from datetime import datetime
import os

# استيراد المكونات
from advanced_agent.autonomous_agent import AutonomousAgent
from depin_network.depin_network import DePINNetwork

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# المتغيرات العامة
agent = None
depin_network = None

async def init_app():
    """تهيئة التطبيق"""
    global agent, depin_network
    
    logger.info("🚀 تهيئة السيرفر...")
    
    # تهيئة الوكيل المستقل
    api_keys = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'google': os.getenv('GOOGLE_API_KEY'),
        'deepseek': os.getenv('DEEPSEEK_API_KEY'),
        'github': os.getenv('GITHUB_TOKEN')
    }
    
    agent = AutonomousAgent(api_keys, '/tmp/ai_agent_storage')
    await agent.initialize()
    
    # تهيئة شبكة DePIN
    depin_network = DePINNetwork()
    
    logger.info("✅ السيرفر جاهز!")

# نقاط API

# 1. تنفيذ أمر
async def execute_command(request):
    """تنفيذ أمر جديد"""
    try:
        data = await request.json()
        command = data.get('command')
        user_id = data.get('user_id', 'anonymous')
        
        logger.info(f"📥 أمر جديد من {user_id}: {command}")
        
        result = await agent.execute_command(command, user_id)
        
        return web.json_response(result)
        
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 2. الحصول على حالة المشروع
async def get_project_status(request):
    """الحصول على حالة مشروع"""
    try:
        project_id = request.match_info.get('project_id')
        
        status = agent.get_project_status(project_id)
        
        if status:
            return web.json_response({"success": True, "project": status})
        else:
            return web.json_response({"success": False, "error": "المشروع غير موجود"}, status=404)
            
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 3. الحصول على جميع المشاريع
async def get_all_projects(request):
    """الحصول على جميع المشاريع"""
    try:
        user_id = request.query.get('user_id')
        
        projects = agent.get_all_projects(user_id)
        
        return web.json_response({
            "success": True,
            "projects": projects,
            "count": len(projects)
        })
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 4. إصلاح أخطاء المشروع
async def fix_project_errors(request):
    """إصلاح أخطاء مشروع"""
    try:
        project_id = request.match_info.get('project_id')
        
        result = await agent.fix_project_errors(project_id)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 5. تسجيل عقدة جديدة
async def register_node(request):
    """تسجيل عقدة جديدة في شبكة DePIN"""
    try:
        data = await request.json()
        
        result = await depin_network.register_node(data)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 6. إرسال مهمة إلى الشبكة
async def submit_task(request):
    """إرسال مهمة إلى شبكة DePIN"""
    try:
        data = await request.json()
        
        result = await depin_network.submit_task(data)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 7. الحصول على حالة المهمة
async def get_task_status(request):
    """الحصول على حالة مهمة"""
    try:
        task_id = request.match_info.get('task_id')
        
        result = await depin_network.get_task_status(task_id)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 8. الحصول على إحصائيات الشبكة
async def get_network_stats(request):
    """الحصول على إحصائيات شبكة DePIN"""
    try:
        result = await depin_network.get_network_stats()
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 9. الحصول على قائمة العقد
async def get_nodes_list(request):
    """الحصول على قائمة العقد"""
    try:
        result = await depin_network.get_nodes_list()
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 10. الحصول على الإحصائيات
async def get_stats(request):
    """الحصول على الإحصائيات العامة"""
    try:
        projects = agent.get_all_projects()
        
        stats = {
            "activeProjects": len([p for p in projects if p['status'] == 'running']),
            "completedTasks": len(agent.completed_tasks),
            "activeNodes": len([n for n in depin_network.nodes.values() if n['status'] == 'active']),
            "performance": 92,
            "totalProjects": len(projects)
        }
        
        return web.json_response({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 11. الحصول على جميع المشاريع (للجدول)
async def get_projects_list(request):
    """الحصول على قائمة المشاريع"""
    try:
        projects = agent.get_all_projects()
        
        return web.json_response({
            "success": True,
            "projects": projects
        })
        
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

# 12. Health Check
async def health_check(request):
    """فحص صحة السيرفر"""
    return web.json_response({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# إعداد التطبيق
async def create_app():
    """إنشاء تطبيق aiohttp"""
    app = web.Application()
    
    # تهيئة التطبيق
    app.on_startup.append(lambda _: init_app())
    
    # إضافة المسارات
    routes = [
        # Agent API
        web.post('/api/agent/execute', execute_command),
        web.get('/api/agent/project/{project_id}', get_project_status),
        web.get('/api/agent/projects', get_all_projects),
        web.post('/api/agent/project/{project_id}/fix', fix_project_errors),
        
        # DePIN Network API
        web.post('/api/depin/node/register', register_node),
        web.post('/api/depin/task/submit', submit_task),
        web.get('/api/depin/task/{task_id}', get_task_status),
        web.get('/api/depin/stats', get_network_stats),
        web.get('/api/depin/nodes', get_nodes_list),
        
        # General API
        web.get('/api/stats', get_stats),
        web.get('/api/projects', get_projects_list),
        web.get('/api/health', health_check),
        
        # Static files
        web.static('/static', 'frontend', name='static'),
        web.get('/', lambda r: web.FileResponse('frontend/index.html')),
    ]
    
    app.add_routes(routes)
    
    # CORS middleware
    @web.middleware
    async def cors_middleware(request, handler):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    app.middlewares.append(cors_middleware)
    
    return app

# تشغيل السيرفر
async def main():
    """تشغيل السيرفر الرئيسي"""
    app = await create_app()
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    
    logger.info("🌐 السيرفر يعمل على http://0.0.0.0:8000")
    logger.info("📊 الواجهة الأمامية: http://localhost:8000")
    logger.info("📚 API Documentation: http://localhost:8000/api/docs")
    
    # الاستمرار في التشغيل
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
