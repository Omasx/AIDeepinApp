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
        
        # المكونات المتقدمة الجديدة
        self.agi_brain = None
        self.human_interceptor = None
        self.key_manager = None
        self.media_alchemy = None

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
        from .multi_ai_coordinator import MultiAICoordinator
        from .github_integrator import GitHubIntegrator
        from .self_healer import SelfHealer
        from .virtual_desktop import VirtualDesktop
        # المكونات الجديدة من DeOS - مسارات موحدة
        try:
            from projects.decentralized_os.agi.agi_brain import AGIBrain
            from projects.decentralized_os.agi.human_interceptor import HumanInterceptor
            from projects.decentralized_os.agi.key_battery import KeyBatteryManager
            from projects.decentralized_os.agi.media_alchemy import MediaAlchemy

            # QuantumOptimizer exists in depin_network
            from projects.ai_agent.backend.depin_network.quantum_optimizer import QuantumOptimizer
        except ImportError:
            from decentralized_os.agi.agi_brain import AGIBrain
            from decentralized_os.agi.human_interceptor import HumanInterceptor
            from decentralized_os.agi.key_battery import KeyBatteryManager
            from decentralized_os.agi.media_alchemy import MediaAlchemy
            from depin_network.quantum_optimizer import QuantumOptimizer
        
        # تهيئة كل مكون
        self.task_orchestrator = TaskOrchestrator()
        self.cloud_executor = CloudExecutor()
        self.quantum_optimizer = QuantumOptimizer()
        self.multi_ai_coordinator = MultiAICoordinator(self.api_keys)
        self.github_integrator = GitHubIntegrator(self.api_keys.get('github'))
        self.self_healer = SelfHealer()
        self.virtual_desktop = VirtualDesktop()
        
        # تهيئة المكونات المتقدمة
        self.agi_brain = AGIBrain()
        self.human_interceptor = HumanInterceptor()
        self.key_manager = KeyBatteryManager()
        self.media_alchemy = MediaAlchemy()

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
                total_tasks = max(project['tasks_total'], 1)
                project['progress'] = int((project['tasks_completed'] / total_tasks) * 100)
                
                # حفظ الحالة
                self._save_project_state(project_id)
            
            # اكتمال المشروع
            project['status'] = 'completed'
            project['completed_at'] = datetime.now().isoformat()
            
            logger.info(f"🎉 اكتمل المشروع: {project_id}")
            
            # نشر النتائج إذا طُلب ذلك
            if project['task_plan'].get('publish'):
                await self._publish_project(project_id)

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
                
            elif task_type == 'ai_query':
                # استعلام AI
                result = await self.multi_ai_coordinator.query(
                    prompt=task.get('prompt', ''),
                    model=task.get('preferred_model')
                )

            elif task_type == 'image_generation':
                # توليد صورة
                result = await self.multi_ai_coordinator.generate_image(
                    prompt=task.get('prompt', ''),
                    size=task.get('size', '1024x1024')
                )

            elif task_type == 'video_processing':
                # معالجة فيديو متقدمة عبر MediaAlchemy
                result = await self.media_alchemy.create_video(
                    script=task.get('description', ''),
                    assets=task.get('assets', []),
                    output_name=task.get('output', 'output.mp4')
                )

            elif task_type == 'web_deployment':
                # نشر موقع
                result = await self.cloud_executor.deploy_website(
                    source_dir=task.get('source_dir', ''),
                    platform=task.get('platform', 'vercel')
                )

            elif task_type == 'database_operation':
                # عملية قاعدة بيانات
                result = await self.cloud_executor.database_operation(
                    operation=task.get('operation', ''),
                    query=task.get('query')
                )

            else:
                # مهمة مخصصة
                result = await self.virtual_desktop.execute_task(task)
            
            return {
                "success": True,
                "result": result,
                "duration": result.get('duration', 0) if isinstance(result, dict) else 0
            }
            
        except Exception as e:
            logger.error(f"خطأ في تنفيذ المهمة: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _estimate_completion_time(self, task_plan: Dict) -> timedelta:
        """
        تقدير وقت الإنجاز
        """
        total_minutes = 0

        for task in task_plan.get('tasks', []):
            task_type = task.get('type')
            complexity = task.get('complexity', 'medium')

            # تقديرات أساسية (بالدقائق)
            base_times = {
                'code_generation': {'simple': 2, 'medium': 10, 'complex': 60},
                'file_creation': {'simple': 0.5, 'medium': 1, 'complex': 2},
                'command_execution': {'simple': 1, 'medium': 5, 'complex': 15},
                'github_operation': {'simple': 2, 'medium': 5, 'complex': 10},
                'ai_query': {'simple': 1, 'medium': 3, 'complex': 10},
                'image_generation': {'simple': 2, 'medium': 5, 'complex': 10},
                'video_processing': {'simple': 10, 'medium': 60, 'complex': 300},
                'web_deployment': {'simple': 5, 'medium': 15, 'complex': 60},
                'database_operation': {'simple': 1, 'medium': 5, 'complex': 30}
            }

            task_time = base_times.get(task_type, {'simple': 5, 'medium': 10, 'complex': 30}).get(complexity, 10)
            total_minutes += task_time

        # إضافة وقت إضافي للتحسين الكمي (محاكاة تحسين 30%)
        total_minutes = int(total_minutes * 0.7)

        return timedelta(minutes=total_minutes)
    
    def _save_project_state(self, project_id: str):
        """حفظ حالة المشروع"""
        try:
            project = self.active_projects[project_id]
            state_file = self.storage_path / f"{project_id}.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(project, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"خطأ في حفظ حالة المشروع: {e}")
    
    async def _publish_project(self, project_id: str):
        """نشر المشروع"""
        project = self.active_projects[project_id]

        logger.info(f"📤 نشر المشروع: {project_id}")

        # نشر على GitHub
        if self.github_integrator:
            await self.github_integrator.publish_project(project)

        # نشر على الويب
        if project.get('deploy_web'):
            await self.cloud_executor.deploy_website(
                source_dir=project.get('output_dir', ''),
                platform='vercel'
            )

    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """الحصول على حالة مشروع"""
        if project_id in self.active_projects:
            return self.active_projects[project_id]

        # محاولة التحميل من القرص
        state_file = self.storage_path / f"{project_id}.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None
    
    def get_all_projects(self, user_id: str = None) -> List[Dict]:
        """الحصول على جميع المشاريع"""
        projects = list(self.active_projects.values())

        if user_id:
            projects = [p for p in projects if p['user_id'] == user_id]

        return projects
    
    async def fix_project_errors(self, project_id: str) -> Dict[str, Any]:
        """إصلاح أخطاء مشروع"""
        project = self.get_project_status(project_id)
        
        if not project:
            return {"success": False, "error": "المشروع غير موجود"}
        
        if not project.get('errors'):
            return {"success": True, "message": "لا توجد أخطاء"}

        logger.info(f"🔧 إصلاح {len(project['errors'])} خطأ في المشروع {project_id}")
        
        fixed_count = 0

        for error_info in project['errors']:
            result = await self.self_healer.auto_fix(
                error_info['task'],
                error_info['error']
            )

            if result['success']:
                fixed_count += 1
        
        return {
            "success": True,
            "fixed_count": fixed_count,
            "total_errors": len(project['errors'])
        }

    async def shutdown(self):
        """إيقاف الوكيل"""
        logger.info("🛑 إيقاف الوكيل المستقل...")

        self.is_running = False

        # حفظ جميع المشاريع النشطة
        for project_id in self.active_projects:
            self._save_project_state(project_id)

        logger.info("✅ تم الإيقاف بنجاح")
