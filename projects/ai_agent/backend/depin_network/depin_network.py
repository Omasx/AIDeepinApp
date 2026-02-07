# depin_network.py - شبكة DePIN اللامركزية
import logging
from typing import Dict, List, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DePINNetwork:
    """
    شبكة DePIN - شبكة لامركزية لتوزيع المهام والموارد
    """
    
    def __init__(self):
        self.nodes = {}
        self.tasks_queue = []
        self.completed_tasks = []
        self.network_stats = {
            "total_nodes": 0,
            "active_nodes": 0,
            "total_capacity": 0,
            "total_tasks": 0
        }
        
    async def register_node(self, node_info: Dict[str, Any]) -> Dict[str, Any]:
        """تسجيل عقدة جديدة في الشبكة"""
        node_id = node_info.get('id', f"node_{len(self.nodes)}")
        
        logger.info(f"📍 تسجيل عقدة جديدة: {node_id}")
        
        self.nodes[node_id] = {
            "id": node_id,
            "address": node_info.get('address'),
            "capacity": node_info.get('capacity', 1000),
            "speed": node_info.get('speed', 100),
            "latency": node_info.get('latency', 10),
            "status": "active",
            "registered_at": datetime.now().isoformat(),
            "tasks_completed": 0,
            "reputation": 100
        }
        
        self.network_stats['total_nodes'] += 1
        self.network_stats['active_nodes'] += 1
        self.network_stats['total_capacity'] += node_info.get('capacity', 1000)
        
        logger.info(f"✅ تم تسجيل العقدة: {node_id}")
        
        return {
            "success": True,
            "node_id": node_id,
            "message": "تم تسجيل العقدة بنجاح"
        }
    
    async def submit_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """إرسال مهمة إلى الشبكة"""
        task_id = f"task_{len(self.tasks_queue)}"
        
        logger.info(f"📤 إرسال مهمة: {task_id}")
        
        task['id'] = task_id
        task['status'] = 'pending'
        task['submitted_at'] = datetime.now().isoformat()
        
        self.tasks_queue.append(task)
        self.network_stats['total_tasks'] += 1
        
        # توزيع المهمة على العقد
        assigned_node = await self._assign_task_to_node(task)
        
        if assigned_node:
            return {
                "success": True,
                "task_id": task_id,
                "assigned_to": assigned_node['id'],
                "message": "تم إسناد المهمة بنجاح"
            }
        else:
            return {
                "success": False,
                "task_id": task_id,
                "error": "لم يتم العثور على عقدة متاحة"
            }
    
    async def _assign_task_to_node(self, task: Dict) -> Dict[str, Any]:
        """إسناد مهمة إلى عقدة"""
        active_nodes = [n for n in self.nodes.values() if n['status'] == 'active']
        
        if not active_nodes:
            return None
        
        # اختيار أفضل عقدة بناءً على السرعة والسعة
        best_node = max(active_nodes, key=lambda n: n['speed'] - n['latency'])
        
        logger.info(f"🎯 إسناد المهمة إلى: {best_node['id']}")
        
        return best_node
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """الحصول على حالة المهمة"""
        for task in self.tasks_queue + self.completed_tasks:
            if task.get('id') == task_id:
                return {
                    "success": True,
                    "task": task
                }
        
        return {
            "success": False,
            "error": "المهمة غير موجودة"
        }
    
    async def get_network_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الشبكة"""
        return {
            "success": True,
            "stats": self.network_stats,
            "nodes": len(self.nodes),
            "pending_tasks": len(self.tasks_queue),
            "completed_tasks": len(self.completed_tasks)
        }
    
    async def get_nodes_list(self) -> Dict[str, Any]:
        """الحصول على قائمة العقد"""
        return {
            "success": True,
            "nodes": list(self.nodes.values()),
            "count": len(self.nodes)
        }
