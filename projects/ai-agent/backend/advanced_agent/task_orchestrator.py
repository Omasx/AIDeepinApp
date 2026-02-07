# task_orchestrator.py - منسق المهام
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskOrchestrator:
    """
    منسق المهام - ينظم وينسق تنفيذ المهام
    """
    
    def __init__(self):
        self.task_templates = self._load_task_templates()
        self.execution_history = []
        
    def _load_task_templates(self) -> Dict[str, Dict]:
        """تحميل قوالب المهام"""
        return {
            "code_generation": {
                "description": "توليد كود برمجي",
                "estimated_time": 30,
                "priority": "high"
            },
            "file_creation": {
                "description": "إنشاء ملف",
                "estimated_time": 10,
                "priority": "medium"
            },
            "command_execution": {
                "description": "تنفيذ أمر",
                "estimated_time": 15,
                "priority": "high"
            },
            "github_operation": {
                "description": "عملية GitHub",
                "estimated_time": 20,
                "priority": "medium"
            },
            "deployment": {
                "description": "نشر التطبيق",
                "estimated_time": 60,
                "priority": "high"
            }
        }
    
    async def create_task_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        إنشاء خطة مهام بناءً على تحليل الأمر
        """
        logger.info("📋 إنشاء خطة مهام...")
        
        command_type = analysis.get('type', 'general')
        
        # إنشاء قائمة المهام
        tasks = []
        
        if command_type == 'create_website':
            tasks = self._create_website_tasks(analysis)
        elif command_type == 'create_app':
            tasks = self._create_app_tasks(analysis)
        elif command_type == 'create_api':
            tasks = self._create_api_tasks(analysis)
        elif command_type == 'create_bot':
            tasks = self._create_bot_tasks(analysis)
        else:
            tasks = self._create_generic_tasks(analysis)
        
        task_plan = {
            "id": f"plan_{datetime.now().timestamp()}",
            "command_type": command_type,
            "tasks": tasks,
            "total_estimated_time": sum(t.get('estimated_time', 30) for t in tasks),
            "publish": analysis.get('publish', False)
        }
        
        logger.info(f"✅ تم إنشاء خطة بـ {len(tasks)} مهمة")
        
        return task_plan
    
    def _create_website_tasks(self, analysis: Dict) -> List[Dict]:
        """إنشاء مهام لموقع ويب"""
        return [
            {
                "type": "code_generation",
                "description": "توليد HTML و CSS و JavaScript",
                "language": "html",
                "framework": "vanilla",
                "estimated_time": 30
            },
            {
                "type": "file_creation",
                "description": "إنشاء ملفات المشروع",
                "estimated_time": 10
            },
            {
                "type": "github_operation",
                "description": "إنشاء مستودع GitHub",
                "operation": "create_repo",
                "params": {
                    "name": analysis.get('project_name', 'website'),
                    "description": analysis.get('description', '')
                },
                "estimated_time": 15
            },
            {
                "type": "github_operation",
                "description": "رفع الملفات",
                "operation": "push",
                "estimated_time": 10
            },
            {
                "type": "command_execution",
                "description": "نشر على Vercel",
                "command": "vercel --prod",
                "estimated_time": 30
            }
        ]
    
    def _create_app_tasks(self, analysis: Dict) -> List[Dict]:
        """إنشاء مهام لتطبيق"""
        return [
            {
                "type": "code_generation",
                "description": "توليد كود التطبيق",
                "language": analysis.get('language', 'python'),
                "framework": analysis.get('framework', 'flask'),
                "estimated_time": 45
            },
            {
                "type": "file_creation",
                "description": "إنشاء ملفات الإعدادات",
                "estimated_time": 15
            },
            {
                "type": "command_execution",
                "description": "تثبيت المكاتب",
                "command": "pip install -r requirements.txt",
                "estimated_time": 20
            },
            {
                "type": "command_execution",
                "description": "اختبار التطبيق",
                "command": "pytest",
                "estimated_time": 15
            }
        ]
    
    def _create_api_tasks(self, analysis: Dict) -> List[Dict]:
        """إنشاء مهام لـ API"""
        return [
            {
                "type": "code_generation",
                "description": "توليد كود API",
                "language": "python",
                "framework": "fastapi",
                "estimated_time": 40
            },
            {
                "type": "file_creation",
                "description": "إنشاء ملفات الإعدادات",
                "estimated_time": 10
            },
            {
                "type": "command_execution",
                "description": "إنشاء قاعدة البيانات",
                "command": "python init_db.py",
                "estimated_time": 15
            }
        ]
    
    def _create_bot_tasks(self, analysis: Dict) -> List[Dict]:
        """إنشاء مهام لـ Bot"""
        return [
            {
                "type": "code_generation",
                "description": "توليد كود البوت",
                "language": "python",
                "estimated_time": 35
            },
            {
                "type": "file_creation",
                "description": "إنشاء ملفات الإعدادات",
                "estimated_time": 10
            }
        ]
    
    def _create_generic_tasks(self, analysis: Dict) -> List[Dict]:
        """إنشاء مهام عامة"""
        return [
            {
                "type": "code_generation",
                "description": "توليد الكود",
                "language": analysis.get('language', 'python'),
                "estimated_time": 30
            },
            {
                "type": "file_creation",
                "description": "إنشاء الملفات",
                "estimated_time": 10
            }
        ]
    
    def optimize_task_order(self, tasks: List[Dict]) -> List[Dict]:
        """
        تحسين ترتيب المهام للأداء الأفضل
        """
        # ترتيب المهام حسب الأولوية والتبعيات
        priority_order = {"high": 0, "medium": 1, "low": 2}
        
        return sorted(
            tasks,
            key=lambda t: priority_order.get(t.get('priority', 'medium'), 1)
        )
    
    def estimate_total_time(self, tasks: List[Dict]) -> int:
        """
        تقدير الوقت الإجمالي
        """
        return sum(t.get('estimated_time', 30) for t in tasks)
    
    def log_execution(self, task: Dict, result: Dict):
        """
        تسجيل تنفيذ المهمة
        """
        self.execution_history.append({
            "task": task,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
