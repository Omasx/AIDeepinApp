import logging
import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("AOI-Layer5-Memory")

class MemorySystem:
    """
    LAYER 5 – Memory System
    المسؤولية: ذاكرة طويلة الأمد، منع تكرار الأخطاء، حفظ تاريخ النظام
    """
    def __init__(self, db_path: str = "projects/aoi_system/memory.db"):
        self.db_path = db_path
        self._init_db()
        logger.info("💾 Memory System Layer initialized.")

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # تاريخ المهام
            cursor.execute('''CREATE TABLE IF NOT EXISTS task_history
                            (id TEXT PRIMARY KEY, description TEXT, status TEXT, result TEXT, timestamp DATETIME)''')
            # ذاكرة الأخطاء
            cursor.execute('''CREATE TABLE IF NOT EXISTS error_memory
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, error_type TEXT, details TEXT, resolution TEXT, timestamp DATETIME)''')
            # حالة النظام الحالية
            cursor.execute('''CREATE TABLE IF NOT EXISTS runtime_state
                            (key TEXT PRIMARY KEY, value TEXT)''')
            conn.commit()

    def record_task(self, task_id: str, desc: str, status: str, result: Any):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO task_history VALUES (?, ?, ?, ?, ?)",
                        (task_id, desc, status, json.dumps(result), datetime.now()))

    def record_error(self, error_type: str, details: str, resolution: str = "unresolved"):
        logger.warning(f"⚠️ Recording error in memory: {error_type}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO error_memory (error_type, details, resolution, timestamp) VALUES (?, ?, ?, ?)",
                        (error_type, details, resolution, datetime.now()))

    def get_runtime_value(self, key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM runtime_state WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def set_runtime_value(self, key: str, value: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO runtime_state VALUES (?, ?)", (key, value))

    def get_past_errors(self, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM error_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [{"type": r[1], "details": r[2], "resolution": r[3]} for r in cursor.fetchall()]
