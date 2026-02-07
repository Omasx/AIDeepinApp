# self_healer.py - نظام الإصلاح الذاتي
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SelfHealer:
    """
    المصلح الذاتي - يكتشف الأخطاء ويصلحها تلقائياً
    """
    
    def __init__(self):
        self.error_patterns = self._load_error_patterns()
        self.fix_history = []
        
    def _load_error_patterns(self) -> Dict[str, Dict]:
        """تحميل أنماط الأخطاء الشائعة"""
        return {
            # أخطاء Python
            "SyntaxError": {
                "description": "خطأ في الصيغة",
                "solutions": ["تحقق من الأقواس والفواصل", "تأكد من المحاذاة"]
            },
            "ImportError": {
                "description": "خطأ في الاستيراد",
                "solutions": ["تثبيت المكتبة المفقودة", "تحقق من اسم المكتبة"]
            },
            "FileNotFoundError": {
                "description": "الملف غير موجود",
                "solutions": ["تحقق من مسار الملف", "أنشئ الملف"]
            },
            # أخطاء JavaScript
            "TypeError": {
                "description": "خطأ في النوع",
                "solutions": ["تحقق من نوع البيانات", "استخدم typeof للتحقق"]
            },
            "ReferenceError": {
                "description": "مرجع غير معرّف",
                "solutions": ["تحقق من تعريف المتغير", "أضف const/let/var"]
            }
        }
    
    async def auto_fix(self, task: Dict, error: str) -> Dict[str, Any]:
        """
        إصلاح تلقائي للخطأ
        """
        logger.info(f"🔧 محاولة إصلاح الخطأ: {error}")
        
        # تحديد نوع الخطأ
        error_type = self._identify_error_type(error)
        
        # البحث عن الحل
        solution = self._find_solution(error_type, error)
        
        if solution:
            logger.info(f"✅ وجدت حل: {solution}")
            
            self.fix_history.append({
                "error": error,
                "error_type": error_type,
                "solution": solution,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "solution": solution,
                "error_type": error_type
            }
        else:
            logger.warning(f"⚠️ لم أستطع إيجاد حل للخطأ")
            
            return {
                "success": False,
                "error": "لم يتم العثور على حل",
                "error_type": error_type
            }
    
    def _identify_error_type(self, error: str) -> str:
        """تحديد نوع الخطأ"""
        error_lower = error.lower()
        
        for error_type in self.error_patterns.keys():
            if error_type.lower() in error_lower:
                return error_type
        
        return "UnknownError"
    
    def _find_solution(self, error_type: str, error: str) -> str:
        """البحث عن حل للخطأ"""
        if error_type in self.error_patterns:
            solutions = self.error_patterns[error_type]['solutions']
            return solutions[0] if solutions else None
        
        return None
    
    async def analyze_failure(self, task: Dict, error: str) -> Dict[str, Any]:
        """
        تحليل فشل المهمة
        """
        logger.info(f"🔍 تحليل فشل المهمة...")
        
        analysis = {
            "task_type": task.get('type'),
            "error": error,
            "error_type": self._identify_error_type(error),
            "possible_causes": self._analyze_causes(task, error),
            "recommendations": self._get_recommendations(task, error)
        }
        
        return analysis
    
    def _analyze_causes(self, task: Dict, error: str) -> list:
        """تحليل الأسباب المحتملة"""
        causes = []
        
        if "not found" in error.lower():
            causes.append("الملف أو المورد غير موجود")
        elif "permission" in error.lower():
            causes.append("مشكلة في الأذونات")
        elif "timeout" in error.lower():
            causes.append("انتهاء المهلة الزمنية")
        elif "connection" in error.lower():
            causes.append("مشكلة في الاتصال")
        
        return causes
    
    def _get_recommendations(self, task: Dict, error: str) -> list:
        """الحصول على التوصيات"""
        recommendations = []
        
        if "not found" in error.lower():
            recommendations.append("تحقق من المسار")
            recommendations.append("أنشئ الملف أو المجلد")
        elif "permission" in error.lower():
            recommendations.append("تحقق من الأذونات")
            recommendations.append("استخدم sudo إذا لزم الأمر")
        
        return recommendations
    
    def get_fix_history(self) -> list:
        """الحصول على سجل الإصلاحات"""
        return self.fix_history
