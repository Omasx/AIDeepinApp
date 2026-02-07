"""
session_manager.py - إدارة الجلسات المجانية
نظام جلسات مجاني بدون blockchain
"""

import hashlib
import time
import json
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class FreeSessionManager:
    """
    نظام جلسات مجاني بدون blockchain
    
    الميزات:
    - إنشاء جلسات مجانية
    - تحقق من الصلاحية
    - إدارة المهام والإحصائيات
    """
    
    def __init__(self, storage_path="./sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.active_sessions = {}
        self.load_sessions()
        logger.info(f"✅ تم تهيئة مدير الجلسات")
    
    def load_sessions(self):
        """تحميل الجلسات الموجودة"""
        for session_file in self.storage_path.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    session = json.load(f)
                    token = session["token"]
                    
                    # التحقق من عدم انتهاء الصلاحية
                    if time.time() < session["expires_at"]:
                        self.active_sessions[token] = session
            except Exception as e:
                logger.warning(f"⚠️ خطأ في تحميل الجلسة: {e}")
    
    def create_free_session(self, device_id: str) -> Dict:
        """
        إنشاء جلسة مجانية
        
        Args:
            device_id: معرف الجهاز
        
        Returns:
            معلومات الجلسة
        """
        timestamp = int(time.time())
        
        # إنشاء token فريد
        session_data = f"{device_id}:{timestamp}:{hash(time.time())}".encode()
        session_token = hashlib.sha256(session_data).hexdigest()
        
        # معلومات الجلسة
        session_info = {
            "device_id": device_id,
            "token": session_token,
            "created_at": timestamp,
            "expires_at": timestamp + (30 * 24 * 3600),  # 30 يوم
            "data_used_mb": 0,
            "connection_count": 0,
            "ai_requests": 0,
            "games_played": 0,
            "apps_created": 0,
            "cost": 0  # مجاني تماماً
        }
        
        # حفظ الجلسة
        self.active_sessions[session_token] = session_info
        self._save_session(session_token, session_info)
        
        logger.info(f"✅ جلسة جديدة: {device_id} → {session_token[:16]}...")
        return session_info
    
    def validate_session(self, token: str) -> bool:
        """
        التحقق من صلاحية الجلسة
        
        Args:
            token: رمز الجلسة
        
        Returns:
            True إذا كانت الجلسة صالحة
        """
        if token in self.active_sessions:
            session = self.active_sessions[token]
            
            # التحقق من انتهاء الصلاحية
            if time.time() < session["expires_at"]:
                return True
            else:
                # حذف الجلسة المنتهية
                self.delete_session(token)
                return False
        
        return False
    
    def get_session(self, token: str) -> Optional[Dict]:
        """الحصول على معلومات الجلسة"""
        if self.validate_session(token):
            return self.active_sessions[token]
        return None
    
    def update_session_stats(self, token: str, **kwargs):
        """تحديث إحصائيات الجلسة"""
        if token in self.active_sessions:
            session = self.active_sessions[token]
            
            # تحديث الحقول
            for key, value in kwargs.items():
                if key in session:
                    if isinstance(session[key], (int, float)):
                        session[key] += value
                    else:
                        session[key] = value
            
            self._save_session(token, session)
    
    def delete_session(self, token: str) -> bool:
        """حذف جلسة"""
        if token in self.active_sessions:
            del self.active_sessions[token]
            
            session_file = self.storage_path / f"{token}.json"
            if session_file.exists():
                session_file.unlink()
            
            logger.info(f"🗑️ تم حذف الجلسة: {token[:16]}...")
            return True
        return False
    
    def _save_session(self, token: str, data: Dict):
        """حفظ الجلسة محلياً"""
        session_file = self.storage_path / f"{token}.json"
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all_sessions(self) -> Dict:
        """الحصول على جميع الجلسات النشطة"""
        # تنظيف الجلسات المنتهية
        expired_tokens = []
        for token, session in self.active_sessions.items():
            if time.time() >= session["expires_at"]:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            self.delete_session(token)
        
        return self.active_sessions
    
    def get_stats(self) -> Dict:
        """إحصائيات النظام"""
        sessions = self.get_all_sessions()
        
        total_ai_requests = sum(s.get("ai_requests", 0) for s in sessions.values())
        total_games = sum(s.get("games_played", 0) for s in sessions.values())
        total_apps = sum(s.get("apps_created", 0) for s in sessions.values())
        total_data = sum(s.get("data_used_mb", 0) for s in sessions.values())
        
        return {
            "active_sessions": len(sessions),
            "total_ai_requests": total_ai_requests,
            "total_games_played": total_games,
            "total_apps_created": total_apps,
            "total_data_used_mb": total_data,
            "total_cost": "0 USD (100% FREE!)"
        }


# ============================================================================
# اختبار
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    manager = FreeSessionManager()
    
    # إنشاء جلسة مجانية
    device_id = "mobile_12345"
    session = manager.create_free_session(device_id)
    
    print(f"\n🎫 معلومات الجلسة:")
    print(f"Device: {session['device_id']}")
    print(f"Token: {session['token'][:32]}...")
    print(f"صالح حتى: {time.ctime(session['expires_at'])}")
    print(f"💰 التكلفة: {session['cost']} SOL (مجاني تماماً!)")
    
    # التحقق من الجلسة
    token = session['token']
    is_valid = manager.validate_session(token)
    print(f"\n✔️ الجلسة صالحة: {is_valid}")
    
    # تحديث الإحصائيات
    manager.update_session_stats(token, ai_requests=5, games_played=2)
    
    print(f"\n📊 الإحصائيات:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
