import psutil
import logging
from typing import Dict

logger = logging.getLogger("DeOS-Monitor")

class SystemMonitor:
    """
    مراقب موارد النظام لـ DeOS.
    """
    def __init__(self):
        logger.info("📡 System Monitor active.")

    async def check_status(self) -> Dict:
        """
        فحص حالة الجهاز والعمليات.
        """
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # محاكاة فحص الشبكة
        network_ok = True

        issues = []
        if cpu > 90: issues.append("High CPU usage")
        if memory > 90: issues.append("Low memory")

        return {
            "healthy": len(issues) == 0,
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "network": "connected" if network_ok else "disconnected",
            "issues": issues
        }
