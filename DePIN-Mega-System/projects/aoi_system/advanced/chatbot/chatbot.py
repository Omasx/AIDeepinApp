import asyncio
from typing import Dict, Any, List
import logging
from datetime import datetime
import time

logger = logging.getLogger("AOI-Advanced-Chatbot")

class IntelligentChatbot:
    """
    الشات بوت الذكي القابل للتحول لوكيل (Agent)
    """
    def __init__(self, llama_system):
        self.llama = llama_system
        self.mode = "chat"  # chat أو agent
        self.conversation_history = []
        self.active_tasks = []
        self.permissions = {
            "internet_access": False,
            "file_access": False,
            "code_execution": False,
            "system_control": False
        }
        
    async def chat(self, message: str, user_id: str) -> Dict[str, Any]:
        logger.info(f"💬 Chat message from {user_id}: {message}")
        
        if self._is_agent_activation_command(message):
            return await self._request_agent_mode_activation(user_id)
        
        self.conversation_history.append({"role": "user", "content": message, "timestamp": datetime.now().isoformat()})
        
        # محاكاة رد Llama
        response = f"أنا هنا لمساعدتك. بخصوص '{message}'، سأقوم بتحليل ذلك."
        
        self.conversation_history.append({"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()})
        
        return {
            "response": response,
            "mode": self.mode,
            "needs_approval": False
        }
    
    def _is_agent_activation_command(self, message: str) -> bool:
        phrases = ["تحول لوكيل", "صير وكيل", "agent mode", "activate agent"]
        return any(p in message.lower() for p in phrases)
    
    async def _request_agent_mode_activation(self, user_id: str) -> Dict[str, Any]:
        return {
            "response": "⚠️ **طلب تفعيل وضع الوكيل**\n\nهل توافق على منحي صلاحيات كاملة للتنفيذ المستقل؟",
            "needs_approval": True,
            "approval_type": "agent_activation",
            "approval_data": {"requested_permissions": ["internet", "files", "code"]}
        }
    
    async def activate_agent_mode(self, approved: bool, user_id: str) -> Dict[str, Any]:
        if not approved:
            return {"success": False, "message": "❌ تم رفض تفعيل وضع الوكيل"}
        
        self.mode = "agent"
        self.permissions = {k: True for k in self.permissions}
        return {
            "success": True,
            "message": "✅ تم تفعيل وضع الوكيل! أنا الآن جاهز لتنفيذ المهام المعقدة.",
            "mode": "agent",
            "show_monitoring_window": True
        }

    async def execute_agent_task(self, task: str, user_id: str) -> Dict[str, Any]:
        if self.mode != "agent":
            return {"error": "يجب تفعيل وضع الوكيل أولاً"}
        
        # محاكاة تحليل المهمة
        is_sensitive = "حذف" in task or "تعديل" in task
        
        if is_sensitive:
            return {
                "response": f"⚠️ هذه المهمة حساسة: {task}. هل أنت متأكد؟",
                "needs_approval": True,
                "approval_type": "sensitive_task",
                "approval_data": {"task": task}
            }
        
        return {
            "success": True,
            "message": f"✅ بدأت تنفيذ المهمة: {task}",
            "show_monitoring_window": True,
            "monitoring_data": {"task_id": f"t_{int(time.time())}", "steps": ["Analysis", "Execution", "Verification"]}
        }
