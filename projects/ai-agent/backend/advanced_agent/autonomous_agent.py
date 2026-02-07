# autonomous_agent.py - الوكيل المستقل الكامل
import asyncio
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutonomousAgent:
    """
    الوكيل المستقل - قادر على:
    1. إنشاء مشاريع كاملة (100+ مهمة)
    2. العمل بشكل مستقل في السحابة
    3. إصلاح الأخطاء تلقائياً
    4. التنسيق مع نماذج AI متعددة
    5. العمل على مدار الساعة
    """
    
    def __init__(self, api_keys: Dict[str, str], storage_path: str):
        self.api_keys = api_keys
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # المكونات
        self.task_orchestrator = None
        self.cloud_executor = None
        self.quantum_optimizer = None
        self.multi_ai_coordinator = None
        self.github_integrator = None
        self.self_healer = None
        self.virtual_desktop = None
        
        # حالة الوكيل
        self.is_running = False
        self.active_projects = {}
        self.completed_tasks = []
        self.failed_tasks = []
        
    async def initialize(self):
        """تهيئة جميع المكونات"""
        logger.info("🚀 تهيئة الوكيل المستقل...")
        
        # استيراد المكونات
        from .task_orchestrator import TaskOrchestrator
        from .cloud_executor import CloudExecutor
        from .quantum_optimizer import QuantumOptimizer
        from .multi_ai_coordinator import MultiAICoordinator
        from .github_integrator import GitHubIntegrator
        from .self_healer import SelfHealer
        from .virtual_desktop import VirtualDesktop
        
        # تهيئة كل مكون
        self.task_orchestrator = TaskOrchestrator()
        self.cloud_executor = CloudExecutor()
        self.quantum_optimizer = QuantumOptimizer()
        self.multi_ai_coordinator = MultiAICoordinator(self.api_keys)
        self.github_integrator = GitHubIntegrator(self.api_keys.get('github'))
        self.self_healer = SelfHealer()
        self.virtual_desktop = VirtualDesktop()
        
        # مزامنة نماذج AI
        await self.multi_ai_coordinator.sync_all_models()
        
        # تهيئة سطح المكتب الافتراضي
        await self.virtual_desktop.initialize()
        
        self.is_running = True
        logger.info("✅ الوكيل جاهز للعمل!")
        
    async def execute_command(self, command: str, user_id: str) -> Dict[str, Any]:
        """
        تنفيذ أمر من المستخدم
        """
        logger.info(f"📥 أمر جديد من {user_id}: {command}")
        
        # المرحلة 1: تحليل الأمر
        analysis = await self.multi_ai_coordinator.analyze_command(command)
        
        # المرحلة 2: إنشاء خطة المهام
        task_plan = await self.task_orchestrator.create_task_plan(analysis)
        
        # المرحلة 3: تقدير الوقت
        estimated_time = self._estimate_completion_time(task_plan)
        
        # إنشاء مشروع
        project_id = f"project_{datetime.now().timestamp()}"
        project = {
            "id": project_id,
            "user_id": user_id,
            "command": command,
            "analysis": analysis,
            "task_plan": task_plan,
            "estimated_time": estimated_time,
            "status": "pending",
            "progress": 0,
            "started_at": datetime.now().isoformat(),
            "estimated_completion": (datetime.now() + estimated_time).isoformat(),
            "tasks_total": len(task_plan.get('tasks', [])),
            "tasks_completed": 0,
            "errors": []
        }
        
        self.active_projects[project_id] = project
        
        # بدء التنفيذ في الخلفية
        asyncio.create_task(self._execute_project(project_id))
        
        return {
            "success": True,
            "project_id": project_id,
            "message": f"تم إنشاء {len(task_plan.get('tasks', []))} مهمة",
            "estimated_time": str(estimated_time),
            "estimated_completion": project['estimated_completion']
        }
    
    async def _execute_project(self, project_id: str):
        """
        تنفيذ مشروع كامل
        """
        project = self.active_projects[project_id]
        
        try:
            logger.info(f"🎯 بدء تنفيذ المشروع: {project_id}")
            
            project['status'] = 'running'
            
            # تنفيذ المهام واحدة تلو الأخرى
            for task_index, task in enumerate(project['task_plan'].get('tasks', [])):
                
                # تحديث التقدم
                project['current_task'] = task
                project['current_task_index'] = task_index
                
                logger.info(f"📌 المهمة {task_index + 1}/{len(project['task_plan'].get('tasks', []))}: {task.get('description', 'مهمة')}")
                
                # تنفيذ المهمة
                result = await self._execute_single_task(task, project)
                
                if result['success']:
                    project['tasks_completed'] += 1
                    self.completed_tasks.append({
                        "project_id": project_id,
                        "task": task,
                        "result": result,
                        "completed_at": datetime.now().isoformat()
                    })
                else:
                    # محاولة الإصلاح الذاتي
                    logger.warning(f"⚠️ فشلت المهمة: {task.get('description', 'مهمة')}")
                    
                    fixed = await self.self_healer.auto_fix(task, result.get('error', ''))
                    
                    if fixed['success']:
                        logger.info(f"✅ تم إصلاح المهمة تلقائياً")
                        project['tasks_completed'] += 1
                    else:
                        project['errors'].append({
                            "task": task,
                            "error": result.get('error', ''),
                            "timestamp": datetime.now().isoformat()
                        })
                        self.failed_tasks.append({
                            "project_id": project_id,
                            "task": task,
                            "error": result.get('error', '')
                        })
                
                # تحديث التقدم
                project['progress'] = int((project['tasks_completed'] / max(project['tasks_total'], 1)) * 100)
                
                # حفظ الحالة
                self._save_project_state(project_id)
            
            # اكتمال المشروع
            project['status'] = 'completed'
            project['completed_at'] = datetime.now().isoformat()
            
            logger.info(f"🎉 اكتمل المشروع: {project_id}")
            
        except Exception as e:
            logger.error(f"❌ خطأ فادح في المشروع {project_id}: {e}")
            project['status'] = 'failed'
            project['fatal_error'] = str(e)
    
    async def _execute_single_task(self, task: Dict, project: Dict) -> Dict[str, Any]:
        """
        تنفيذ مهمة واحدة
        """
        task_type = task.get('type')
        
        try:
            if task_type == 'code_generation':
                # توليد الكود
                result = await self.multi_ai_coordinator.generate_code(
                    description=task.get('description', ''),
                    language=task.get('language', 'python'),
                    framework=task.get('framework')
                )
                
            elif task_type == 'file_creation':
                # إنشاء ملف
                result = await self.cloud_executor.create_file(
                    path=task.get('path', ''),
                    content=task.get('content', '')
                )
                
            elif task_type == 'command_execution':
                # تنفيذ أمر
                result = await self.cloud_executor.execute_command(
                    command=task.get('command', ''),
                    cwd=task.get('working_dir')
                )
                
            elif task_type == 'github_operation':
                # عملية GitHub
                result = await self.github_integrator.execute_operation(
                    operation=task.get('operation', ''),
                    params=task.get('params', {})
                )
                
            else:
                result = {"success": False, "error": f"نوع مهمة غير معروف: {task_type}"}
            
            return result
            
        except Exception as e:
            logger.error(f"خطأ في تنفيذ المهمة: {e}")
            return {"success": False, "error": str(e)}
    
    def _estimate_completion_time(self, task_plan: Dict) -> timedelta:
        """
        تقدير وقت إكمال المشروع
        """
        tasks_count = len(task_plan.get('tasks', []))
        # افتراض 30 ثانية لكل مهمة
        estimated_seconds = tasks_count * 30
        return timedelta(seconds=estimated_seconds)
    
    def _save_project_state(self, project_id: str):
        """
        حفظ حالة المشروع
        """
        try:
            project = self.active_projects[project_id]
            state_file = self.storage_path / f"{project_id}.json"
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(project, f, ensure_ascii=False, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"خطأ في حفظ حالة المشروع: {e}")
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """
        الحصول على حالة مشروع
        """
        return self.active_projects.get(project_id)
    
    def get_all_projects(self, user_id: str = None) -> List[Dict[str, Any]]:
        """
        الحصول على جميع المشاريع
        """
        if user_id:
            return [p for p in self.active_projects.values() if p['user_id'] == user_id]
        return list(self.active_projects.values())
    
    async def fix_project_errors(self, project_id: str) -> Dict[str, Any]:
        """
        إصلاح أخطاء مشروع
        """
        project = self.active_projects.get(project_id)
        
        if not project:
            return {"success": False, "error": "المشروع غير موجود"}
        
        logger.info(f"🔧 إصلاح أخطاء المشروع: {project_id}")
        
        fixed_count = 0
        for error in project.get('errors', []):
            fixed = await self.self_healer.auto_fix(error['task'], error['error'])
            if fixed['success']:
                fixed_count += 1
        
        return {
            "success": True,
            "fixed": fixed_count,
            "total_errors": len(project.get('errors', []))
        }
