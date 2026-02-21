# task_orchestrator.py - منسق المهام الذكي
import json
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskOrchestrator:
    """
    منسق المهام - يحول الأوامر إلى خطط تنفيذ مفصلة (100+ مهمة)
    """
    
    def __init__(self):
        self.task_templates = self._load_task_templates()
    
    def _load_task_templates(self) -> Dict:
        """تحميل قوالب المهام"""
        return {
            "website": self._get_website_template(),
            "mobile_app": self._get_mobile_app_template(),
            "ai_model": self._get_ai_model_template(),
            "game": self._get_game_template(),
            "api": self._get_api_template(),
            "data_processing": self._get_data_processing_template()
        }
    
    async def create_task_plan(self, analysis: Dict) -> Dict[str, Any]:
        """
        إنشاء خطة مهام مفصلة
        """
        project_type = analysis.get('project_type', 'custom')
        requirements = analysis.get('requirements', {})
        
        logger.info(f"📋 إنشاء خطة مهام لمشروع من نوع: {project_type}")
        
        if project_type in self.task_templates:
            # استخدام قالب موجود
            template = self.task_templates[project_type]
            tasks = self._expand_template(template, requirements)
        else:
            # إنشاء مهام مخصصة
            tasks = await self._generate_custom_tasks(analysis)
        
        task_plan = {
            "id": f"plan_{datetime.now().timestamp()}",
            "project_type": project_type,
            "tasks": tasks,
            "total_tasks": len(tasks),
            "dependencies": self._analyze_dependencies(tasks),
            "critical_path": self._find_critical_path(tasks),
            "publish": analysis.get('publish', True)
        }
        
        logger.info(f"✅ تم إنشاء خطة بـ {len(tasks)} مهمة")
        
        return task_plan
    
    def _get_website_template(self) -> List[Dict]:
        """قالب إنشاء موقع احترافي ضخم"""
        tasks = [
            # المرحلة 1: التخطيط (10 مهام)
            {"id": 1, "type": "ai_query", "description": "تحليل متطلبات الموقع السوقية", "complexity": "simple"},
            {"id": 2, "type": "ai_query", "description": "دراسة المنافسين وتحديد المميزات التنافسية", "complexity": "simple"},
            {"id": 3, "type": "ai_query", "description": "إنشاء خريطة الموقع الكاملة (Sitemap)", "complexity": "simple"},
            {"id": 4, "type": "ai_query", "description": "تحديد هيكلية البيانات وقواعد البيانات", "complexity": "medium"},
            {"id": 5, "type": "ai_query", "description": "تصميم تدفق المستخدم (User Flow)", "complexity": "medium"},
            {"id": 6, "type": "ai_query", "description": "تحديد التقنيات (Stack Selection)", "complexity": "simple"},
            {"id": 7, "type": "ai_query", "description": "كتابة مواصفات واجهة البرمجة (API Specs)", "complexity": "medium"},
            {"id": 8, "type": "ai_query", "description": "تخطيط استراتيجية المحتوى SEO", "complexity": "medium"},
            {"id": 9, "type": "ai_query", "description": "تحديد معايير الأمان والحماية", "complexity": "medium"},
            {"id": 10, "type": "ai_query", "description": "إعداد خطة الاختبار الشاملة", "complexity": "simple"},
            
            # المرحلة 2: التصميم والهوية (10 مهام)
            {"id": 11, "type": "image_generation", "description": "توليد شعار الموقع باحترافية", "complexity": "medium"},
            {"id": 12, "type": "image_generation", "description": "إنشاء أيقونات مخصصة للموقع", "complexity": "medium"},
            {"id": 13, "type": "code_generation", "description": "تحديد نظام الألوان والخطوط (Design System)", "complexity": "simple"},
            {"id": 14, "type": "image_generation", "description": "توليد صور الخلفية والـ Hero section", "complexity": "medium"},
            {"id": 15, "type": "image_generation", "description": "تصميم واجهات الموبايل", "complexity": "complex"},
            {"id": 16, "type": "image_generation", "description": "تصميم واجهات سطح المكتب", "complexity": "complex"},
            {"id": 17, "type": "image_generation", "description": "تصميم الرسوم التوضيحية", "complexity": "medium"},
            {"id": 18, "type": "image_generation", "description": "تصميم واجهة لوحة التحكم", "complexity": "complex"},
            {"id": 19, "type": "image_generation", "description": "إنشاء Favicon وعناصر البراند", "complexity": "simple"},
            {"id": 20, "type": "ai_query", "description": "مراجعة وتحسين التصميم النهائي", "complexity": "medium"},
            
            # المرحلة 3: تطوير الـ Frontend (20 مهمة)
            {"id": 21, "type": "code_generation", "description": "إعداد بيئة React/Next.js", "complexity": "medium", "language": "javascript"},
            {"id": 22, "type": "code_generation", "description": "برمجة مكونات الـ Layout", "complexity": "medium", "language": "jsx"},
            {"id": 23, "type": "code_generation", "description": "تصميم الـ Navigation bar المتجاوب", "complexity": "medium", "language": "jsx"},
            {"id": 24, "type": "code_generation", "description": "بناء الـ Hero Section مع حركات سينمائية", "complexity": "complex", "language": "jsx"},
            {"id": 25, "type": "code_generation", "description": "تطوير صفحة الخدمات", "complexity": "medium", "language": "jsx"},
            {"id": 26, "type": "code_generation", "description": "بناء قسم 'من نحن' بتصميم فريد", "complexity": "medium", "language": "jsx"},
            {"id": 27, "type": "code_generation", "description": "تطوير صفحة التواصل مع التحقق من البيانات", "complexity": "medium", "language": "jsx"},
            {"id": 28, "type": "code_generation", "description": "برمجة الفوتر (Footer) الاحترافي", "complexity": "simple", "language": "jsx"},
            {"id": 29, "type": "code_generation", "description": "إضافة تأثيرات التمرير (Scroll animations)", "complexity": "complex", "language": "javascript"},
            {"id": 30, "type": "code_generation", "description": "دمج الصور المولدة في الموقع", "complexity": "medium", "language": "html"},
            # ... يمكن إضافة المزيد ليصل لـ 100
        ]
        
        # إضافة مهام إضافية تلقائياً للوصول لعدد كبير
        for i in range(31, 101):
            tasks.append({
                "id": i,
                "type": "code_generation",
                "description": f"تحسين واجهة المستخدم - الجزء {i}",
                "complexity": "medium",
                "language": "javascript"
            })
            
        return tasks
    
    def _get_ai_model_template(self) -> List[Dict]:
        """قالب بناء نموذج AI من الصفر"""
        return [
            {"id": 1, "type": "ai_query", "description": "تحديد معمارية النموذج العصبي", "complexity": "medium"},
            {"id": 2, "type": "code_generation", "description": "سكريبت جمع البيانات الضخمة", "complexity": "complex"},
            {"id": 3, "type": "command_execution", "description": "تنظيف ومعالجة البيانات", "complexity": "complex"},
            {"id": 4, "type": "code_generation", "description": "بناء طبقات النموذج (Layers Configuration)", "complexity": "complex"},
            {"id": 5, "type": "command_execution", "description": "بدء عملية التدريب (Training)", "complexity": "complex"},
            {"id": 6, "type": "command_execution", "description": "التحقق من الدقة (Validation)", "complexity": "medium"},
            {"id": 7, "type": "code_generation", "description": "تحسين المعاملات (Hyperparameter Tuning)", "complexity": "complex"},
            {"id": 8, "type": "command_execution", "description": "اختبار النموذج النهائي", "complexity": "medium"},
            {"id": 9, "type": "code_generation", "description": "إنشاء واجهة API للنموذج", "complexity": "medium"},
            {"id": 10, "type": "web_deployment", "description": "نشر النموذج في السحابة", "complexity": "medium"}
        ]
    
    def _get_mobile_app_template(self) -> List[Dict]:
        """قالب تطبيق موبايل احترافي"""
        return [
            {"id": 1, "type": "ai_query", "description": "تخطيط تجربة المستخدم (UX Design)", "complexity": "medium"},
            {"id": 2, "type": "code_generation", "description": "إعداد مشروع Flutter/React Native", "complexity": "medium"},
            {"id": 3, "type": "code_generation", "description": "بناء نظام التنقل (Navigation)", "complexity": "medium"},
            {"id": 4, "type": "code_generation", "description": "برمجة واجهة تسجيل الدخول والمصادقة", "complexity": "complex"},
            {"id": 5, "type": "code_generation", "description": "تطوير الشاشة الرئيسية", "complexity": "complex"},
            {"id": 6, "type": "code_generation", "description": "دمج خدمات التخزين السحابي", "complexity": "medium"},
            {"id": 7, "type": "code_generation", "description": "إضافة الإشعارات (Push Notifications)", "complexity": "medium"},
            {"id": 8, "type": "command_execution", "description": "اختبار الأداء على المحاكي", "complexity": "medium"},
            {"id": 9, "type": "command_execution", "description": "بناء ملف APK/IPA", "complexity": "complex"},
            {"id": 10, "type": "github_operation", "description": "رفع الكود المصدري", "complexity": "simple"}
        ]
    
    def _get_game_template(self) -> List[Dict]:
        """قالب تطوير لعبة"""
        return [
            {"id": 1, "type": "ai_query", "description": "تصميم ميكانيكا اللعبة", "complexity": "medium"},
            {"id": 2, "type": "code_generation", "description": "برمجة محرك الفيزياء", "complexity": "complex"},
            {"id": 3, "type": "image_generation", "description": "توليد الشخصيات والعناصر", "complexity": "complex"},
            {"id": 4, "type": "code_generation", "description": "بناء المستويات (Level Design)", "complexity": "complex"}
        ]
    
    def _get_api_template(self) -> List[Dict]:
        """قالب تطوير API"""
        return [
            {"id": 1, "type": "code_generation", "description": "تصميم قاعدة البيانات (Schema)", "complexity": "medium"},
            {"id": 2, "type": "code_generation", "description": "برمجة الـ Endpoints الأساسية", "complexity": "complex"},
            {"id": 3, "type": "code_generation", "description": "نظام الأمان وJWT", "complexity": "complex"},
            {"id": 4, "type": "command_execution", "description": "توثيق الـ API (Swagger)", "complexity": "medium"}
        ]
    
    def _get_data_processing_template(self) -> List[Dict]:
        """قالب معالجة بيانات ضخمة"""
        return [
            {"id": 1, "type": "code_generation", "description": "سكريبت سحب البيانات (Scraping)", "complexity": "complex"},
            {"id": 2, "type": "command_execution", "description": "تحويل الصيغ ومعالجة التكرار", "complexity": "medium"},
            {"id": 3, "type": "ai_query", "description": "تحليل البيانات واستخراج الأنماط", "complexity": "complex"}
        ]
    
    def _expand_template(self, template: List[Dict], requirements: Dict) -> List[Dict]:
        """توسيع القالب بناءً على المتطلبات"""
        expanded_tasks = []
        for task in template:
            expanded_task = task.copy()
            # إضافة تفاصيل مخصصة إذا وجدت
            if requirements.get('custom_feature') and task['id'] == 30:
                expanded_task['description'] += f" مع ميزة {requirements['custom_feature']}"
            expanded_tasks.append(expanded_task)
        return expanded_tasks
    
    async def _generate_custom_tasks(self, analysis: Dict) -> List[Dict]:
        """توليد مهام مخصصة للمشاريع غير التقليدية"""
        # يمكن استدعاء AI هنا لتوليد القائمة
        return [
            {"id": 1, "type": "ai_query", "description": "دراسة الجدوى التقنية", "complexity": "simple"},
            {"id": 2, "type": "code_generation", "description": "بناء النموذج الأولي (Prototype)", "complexity": "complex"},
            {"id": 3, "type": "command_execution", "description": "اختبار المفهوم (POC)", "complexity": "medium"}
        ]
    
    def _analyze_dependencies(self, tasks: List[Dict]) -> Dict:
        """تحليل التبعيات بين المهام"""
        dependencies = {}
        for task in tasks:
            task_id = task['id']
            # افتراض بسيط: كل مهمة تعتمد على سابقتها في نفس المرحلة
            if task_id > 1:
                dependencies[task_id] = [task_id - 1]
            else:
                dependencies[task_id] = []
        return dependencies
    
    def _find_critical_path(self, tasks: List[Dict]) -> List[int]:
        """إيجاد المسار الحرج"""
        return [task['id'] for task in tasks]
