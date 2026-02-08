# supreme_controller.py - عقدة التحكم العليا (Supreme Control Node)
import asyncio
import logging
from typing import Dict, List, Any
from ..llama_cloud.deepseek_p2p import DeepSeekOrchestrator
from ..llama_cloud.dual_llama_system import DualLlamaAGISystem

logger = logging.getLogger("Supreme-Control")

class SupremeControlNode:
    """
    عقدة التحكم العليا (Supreme Control Node)
    المسؤولية: قيادة وتنسيق جميع الوكلاء السحابيين (Llama & DeepSeek)

    الهيكل:
    - القائد الأعلى: DeepSeek-R1 (التفكير الاستراتيجي والمنطق المعقد)
    - رئيس التخطيط: Llama Instance 1 (تحويل الاستراتيجية إلى خطوات)
    - رئيس التنفيذ: Llama Instance 2 (تحويل الخطوات إلى أفعال)
    """

    def __init__(self, user_email: str):
        self.user_email = user_email
        self.deepseek = DeepSeekOrchestrator()
        self.llama_system = DualLlamaAGISystem(user_email)
        self.is_active = False

    async def boot_all_agents(self):
        """تشغيل جميع الوكلاء في السحابة"""
        logger.info("🌌 Booting Supreme Multi-Agent System...")
        await asyncio.gather(
            self.deepseek.boot_up(),
            self.llama_system.initialize_on_login({"email": self.user_email})
        )
        self.is_active = True
        logger.info("👑 Supreme Control Node is now commanding the cluster.")

    async def execute_supreme_goal(self, goal: str) -> Dict[str, Any]:
        """
        دورة القيادة العليا:
        1. DeepSeek-R1: يحلل الهدف استراتيجياً (المنطق الأعلى)
        2. Llama Instance 1: ينشئ الخطة التنفيذية
        3. Llama Instance 2: ينفذ الخطة
        """
        if not self.is_active:
            await self.boot_all_agents()

        logger.info(f"🔱 Command: {goal}")

        # المرحلة 1: التفكير الاستراتيجي (DeepSeek)
        strategy = await self.deepseek.ask_deepseek(goal)
        logger.info(f"🧠 Strategy defined by DeepSeek-R1")

        # المرحلة 2: التخطيط والتنفيذ (Llama System)
        # نقوم بتمرير استراتيجية DeepSeek إلى Llama كجزء من السياق
        execution_result = await self.llama_system.execute_task_collaborative(
            f"Strategy: {strategy} | Objective: {goal}"
        )

        return {
            "commander": "DeepSeek-R1 (671B)",
            "strategy": strategy,
            "execution": execution_result,
            "status": "Goal achieved via decentralized collaboration",
            "total_cloud_nodes": 102 # 100 P2P nodes + 2 Llama nodes
        }

    def get_cluster_status(self) -> Dict[str, Any]:
        return {
            "control_node": "active",
            "deepseek_p2p_nodes": len(self.deepseek.network.nodes),
            "llama_instances": 2,
            "local_load": "0.0% (Total Cloud Operation)"
        }
