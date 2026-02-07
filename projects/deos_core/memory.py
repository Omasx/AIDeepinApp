import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger("DeOS-Memory")

class LongTermMemory:
    """
    نظام الذاكرة الدائمة لـ DeOS.
    يحفظ الأهداف، القرارات، والنتائج للتعلم المستمر.
    """
    def __init__(self, storage_file: str = "projects/deos_core/memory_storage.json"):
        self.storage_file = storage_file
        self.data = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading memory: {e}")

        return {
            "goals": [],
            "history": [],
            "performance_metrics": {},
            "learned_strategies": {}
        }

    def _save(self):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving memory: {e}")

    def get_active_goal(self) -> Optional[str]:
        for goal in self.data["goals"]:
            if goal.get("status") == "active":
                return goal["description"]
        return None

    def add_goal(self, description: str):
        self.data["goals"].append({
            "description": description,
            "status": "active",
            "created_at": datetime.now().isoformat()
        })
        self._save()

    def record_execution(self, task: str, result: Dict):
        self.data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result
        })
        self._save()

    async def evaluate_performance(self):
        """
        تحليل النتائج السابقة لتحسين الأداء المستقبلي.
        """
        logger.info("🧠 Evaluating recent performance to update strategies...")
        # منطق بسيط للتحليل
        success_count = sum(1 for h in self.data["history"][-10:] if h["result"]["status"] == "success")
        logger.info(f"📈 Success rate in last 10 tasks: {success_count * 10}%")

        # تحديث الاستراتيجيات بناءً على النجاح
        self.data["performance_metrics"]["last_success_rate"] = success_count / 10 if len(self.data["history"]) > 0 else 0
        self._save()
