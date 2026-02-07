import time
import logging
from pathlib import Path

class HumanInterceptor:
    """
    جسر التدخل البشري - يُستخدم لتجاوز "أنا لست روبوت" والمشاكل المعقدة.
    """

    def __init__(self, flag_dir: str = "projects/decentralized_os/agi/flags"):
        self.flag_dir = Path(flag_dir)
        self.flag_dir.mkdir(parents=True, exist_ok=True)
        self.intervention_flag = self.flag_dir / "NEED_HUMAN.lock"

    def request_help(self, reason: str):
        """
        طلب المساعدة من المستخدم وإيقاف التنفيذ.
        """
        logging.warning(f"🆘 طلب تدخل بشري! السبب: {reason}")
        with open(self.intervention_flag, 'w') as f:
            f.write(reason)

        print("\n" + "!" * 50)
        print(f"⚠️ تنبيه: {reason}")
        print("يرجى حل المشكلة (مثل الكابتشا) ثم حذف ملف المتابعة.")
        print("!" * 50 + "\n")

    def wait_for_clearance(self, timeout_sec: int = 300):
        """
        الانتظار حتى يقوم المستخدم بحل المشكلة وحذف العلم.
        """
        start_time = time.time()
        while self.intervention_flag.exists():
            if time.time() - start_time > timeout_sec:
                logging.error("⏰ انتهى وقت الانتظار للتدخل البشري.")
                return False
            time.sleep(2)

        logging.info("✅ تم الحصول على الموافقة البشرية. المتابعة...")
        return True

    def is_stuck(self) -> bool:
        return self.intervention_flag.exists()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bridge = HumanInterceptor()
    # محاكاة كابتشا
    bridge.request_help("تجاوز اختبار 'أنا لست روبوت' في موقع Adobe")
    # في الواقع، سينتظر هنا حتى يحذف المستخدم الملف
    # bridge.wait_for_clearance()
