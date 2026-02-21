# crdt_engine.py - مزامنة الحالة الكمية بدون تصادم
import time
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("Phantom-Sync")

class QuantumCRDT:
    """
    محرك CRDT لضمان مزامنة الحالة عبر جميع العقد بدون تأخير المصافحة.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state = {} # LWW-Element-Set (Last Write Wins) محاكاة
        self.vector_clock = {node_id: 0}

    def update_state(self, key: str, value: Any):
        """تحديث الحالة محلياً مع طابع زمني"""
        timestamp = time.time()
        self.vector_clock[self.node_id] += 1
        self.state[key] = {"value": value, "ts": timestamp, "node": self.node_id}
        logger.info(f"🔄 تحديث الحالة: {key} = {value}")

    def merge_states(self, remote_state: Dict[str, Any]):
        """دمج الحالة القادمة من عقدة أخرى"""
        for key, remote_data in remote_state.items():
            local_data = self.state.get(key)
            if not local_data or remote_data["ts"] > local_data["ts"]:
                self.state[key] = remote_data
                logger.info(f"🤝 دمج الحالة للعنصر: {key}")

    def get_full_state(self) -> Dict[str, Any]:
        return self.state

if __name__ == "__main__":
    node1 = QuantumCRDT("phone_1")
    node2 = QuantumCRDT("cloud_node_a")
    
    node1.update_state("mission_status", "Active")
    node2.merge_states(node1.get_full_state())
    print(f"Node 2 State: {node2.get_full_state()}")
