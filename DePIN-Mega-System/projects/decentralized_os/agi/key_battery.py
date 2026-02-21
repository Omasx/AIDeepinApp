import json
import logging
from typing import List, Dict

class KeyBatteryManager:
    """
    إدارة مفاتيح الـ AI كمصادر طاقة (Batteries).
    يقوم بتبديل المفاتيح تلقائياً عند نفاد الرصيد أو حدوث أخطاء.
    """
    
    def __init__(self, keys_file: str = "projects/decentralized_os/agi/keys_pool.json"):
        self.keys_file = keys_file
        self.pools = self._load_pools()
        self.active_keys = {}

    def _load_pools(self) -> Dict[str, List[str]]:
        try:
            with open(self.keys_file, 'r') as f:
                return json.load(f)
        except:
            # تجمع مفاتيح افتراضي للمحاكاة
            return {
                "openai": ["key_1_active", "key_2_backup", "key_3_backup"],
                "anthropic": ["ant_key_A", "ant_key_B"],
                "google": ["gemini_1", "gemini_2"]
            }

    def get_fresh_key(self, provider: str) -> str:
        """
        تبديل البطارية (المفتاح) بمفتاح جديد.
        """
        pool = self.pools.get(provider, [])
        if not pool:
            logging.error(f"❌ نفدت بطاريات (مفاتيح) المزود: {provider}")
            return None
        
        # اختيار المفتاح التالي (دائري)
        new_key = pool.pop(0)
        pool.append(new_key) # وضعه في آخر القائمة لإعادة الاستخدام لاحقاً
        
        self.active_keys[provider] = new_key
        logging.info(f"🔋 تم تبديل مفتاح {provider} بنجاح.")
        return new_key

    def report_failure(self, provider: str, error_code: int):
        """
        الإبلاغ عن فشل مفتاح لتشغيل عملية التبديل.
        """
        if error_code in [401, 429]:
            logging.warning(f"⚠️ المفتاح الحالي لـ {provider} ضعيف أو منتهي (Code {error_code}).")
            return self.get_fresh_key(provider)
        return self.active_keys.get(provider)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = KeyBatteryManager()
    key = manager.get_fresh_key("openai")
    print(f"Active Key: {key}")
    # محاكاة فشل
    new_key = manager.report_failure("openai", 429)
    print(f"New Key: {new_key}")
