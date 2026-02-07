# scaling_manager.py - نظام التوسع التلقائي
import asyncio
from typing import Dict, List, Any
import logging
import psutil

logger = logging.getLogger(__name__)

class AutoScalingManager:
    """
    مدير التوسع التلقائي لشبكة DePIN
    """

    def __init__(self):
        self.cpu_threshold = 80
        self.active_nodes = [{"id": "node_1", "status": "active"}]
        self.is_monitoring = False

    async def start_monitoring(self):
        """بدء المراقبة المستمرة لأداء الشبكة السحابية"""
        self.is_monitoring = True
        while self.is_monitoring:
            cpu = psutil.cpu_percent()
            if cpu > self.cpu_threshold:
                logger.info(f"📈 تجاوز العتبة ({cpu}%) - إضافة عقدة سحابية جديدة")
                self.active_nodes.append({"id": f"node_{len(self.active_nodes)+1}", "status": "active"})
            await asyncio.sleep(60)

    def get_network_status(self) -> Dict[str, Any]:
        return {"nodes_count": len(self.active_nodes), "cpu_load": psutil.cpu_percent()}
