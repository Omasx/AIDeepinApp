import logging
import traceback
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from loguru import logger as loguru_logger
from typing import Callable, Any

# إعداد Loguru
import sys
loguru_logger.remove()
loguru_logger.add(sys.stderr, level="INFO")
loguru_logger.add("projects/aoi_system/logs/error.log", rotation="10 MB", level="ERROR")

class SelfHealingLayer:
    """
    LAYER 6 – Error Analysis & Self-Healing
    المسؤولية: منع موت النظام، التعافي الذاتي
    """
    def __init__(self, memory_system):
        self.memory = memory_system
        loguru_logger.info("🔧 Self-Healing & Error Analysis Layer initialized.")

    def analyze_exception(self, e: Exception):
        """
        تحليل الخطأ وتخزينه في ذاكرة الأخطاء.
        """
        error_type = type(e).__name__
        details = traceback.format_exc()
        loguru_logger.error(f"🚨 Detected Exception: {error_type}")

        # تخزين في الذاكرة للتعلم لاحقاً
        self.memory.record_error(error_type, details)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def run_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        تشغيل دالة مع استراتيجية إعادة محاولة ذكية.
        """
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            self.analyze_exception(e)
            raise e

    async def reboot_module(self, module_name: str):
        """
        إعادة تشغيل وحدة منهارة.
        """
        loguru_logger.warning(f"♻️ Rebooting module: {module_name}")
        # منطق إعادة التشغيل
        return True
