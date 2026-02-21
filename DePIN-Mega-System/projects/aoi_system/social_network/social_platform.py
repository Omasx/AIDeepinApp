# social_platform.py - الشبكة الاجتماعية الداخلية
import asyncio
from typing import Dict, List, Any
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DePINSocialPlatform:
    """
    شبكة اجتماعية لامركزية داخل التطبيق
    """
    
    def __init__(self):
        self.posts_index = {}
        
    async def create_post(self, user_did: str, content: str, post_type: str = "post") -> Dict[str, Any]:
        logger.info(f"📝 إنشاء {post_type} لـ {user_did}")
        
        post_id = f"post_{int(datetime.now().timestamp())}"
        post = {
            "id": post_id,
            "user_did": user_did,
            "content": content,
            "type": post_type,
            "timestamp": datetime.now().isoformat(),
            "likes": 0
        }
        
        self.posts_index[post_id] = post
        return {"success": True, "post_id": post_id}
    
    async def get_feed(self, user_did: str) -> List[Dict]:
        logger.info(f"📰 جلب Feed لـ {user_did}")
        return list(self.posts_index.values())
    
    async def like_post(self, user_did: str, post_id: str) -> Dict:
        if post_id in self.posts_index:
            self.posts_index[post_id]["likes"] += 1
            return {"success": True, "total_likes": self.posts_index[post_id]["likes"]}
        return {"success": False, "error": "Not found"}
