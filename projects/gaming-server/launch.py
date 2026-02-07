"""
launch.py - سكريبت تشغيل النظام الكامل

هذا الملف يقوم بـ:
1. التحقق من المتطلبات
2. تشغيل IPFS daemon
3. تشغيل السيرفر الرئيسي
4. عرض معلومات النظام
"""

import asyncio
import subprocess
import time
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# استيراد المكونات
from depin_game_server import DePINGameServer
from solana_auth import SolanaAuth
from ipfs_storage import IPFSStorageManager
from quantum_compression import QuantumInspiredCompressor

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()


class DePINLauncher:
    """
    مشغل النظام الكامل
    
    المسؤوليات:
    - التحقق من المتطلبات
    - تشغيل الخدمات المختلفة
    - عرض معلومات النظام
    - إدارة دورة حياة التطبيق
    """
    
    def __init__(self):
        """تهيئة المشغل"""
        self.server = None
        self.auth = None
        self.storage = None
        self.compressor = None
        
        logger.info("="*70)
        logger.info("🚀 DePIN Cloud Gaming Server - Launcher")
        logger.info("="*70)
    
    def check_dependencies(self) -> bool:
        """
        التحقق من المتطلبات
        
        Returns:
            True إذا كانت جميع المتطلبات موجودة
        """
        logger.info("\n🔍 جاري التحقق من المتطلبات...")
        
        required_commands = {
            "python3": "python3 --version",
            "ffmpeg": "ffmpeg -version",
            "ipfs": "ipfs version"
        }
        
        missing = []
        
        for name, cmd in required_commands.items():
            try:
                result = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    check=True,
                    timeout=5
                )
                logger.info(f"✅ {name} متوفر")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                logger.warning(f"⚠️ {name} غير متوفر")
                missing.append(name)
        
        if missing:
            logger.error(f"\n❌ المتطلبات المفقودة: {', '.join(missing)}")
            logger.info("\n💡 تثبيت المتطلبات:")
            logger.info("   Ubuntu/Debian: sudo apt install ffmpeg go-ipfs")
            logger.info("   macOS: brew install ffmpeg ipfs")
            return False
        
        logger.info("✅ جميع المتطلبات موجودة\n")
        return True
    
    def start_ipfs_daemon(self) -> bool:
        """
        تشغيل IPFS daemon
        
        Returns:
            True إذا نجح التشغيل
        """
        logger.info("🌐 تشغيل IPFS daemon...")
        
        try:
            # التحقق من تهيئة IPFS
            ipfs_path = Path.home() / ".ipfs"
            if not ipfs_path.exists():
                logger.info("   تهيئة IPFS للمرة الأولى...")
                subprocess.run(["ipfs", "init"], check=True, capture_output=True)
            
            # تشغيل daemon
            self.ipfs_process = subprocess.Popen(
                ["ipfs", "daemon"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # الانتظار قليلاً لتشغيل الخدمة
            time.sleep(3)
            
            logger.info("✅ IPFS يعمل\n")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ تعذر تشغيل IPFS: {e}")
            logger.info("   يمكنك تشغيل IPFS يدوياً: ipfs daemon\n")
            return False
    
    def initialize_components(self):
        """تهيئة مكونات النظام"""
        logger.info("⚙️ تهيئة مكونات النظام...\n")
        
        # تهيئة السيرفر
        self.server = DePINGameServer(
            host=os.getenv("SERVER_HOST", "0.0.0.0"),
            port=int(os.getenv("SERVER_PORT", 8080))
        )
        
        # تهيئة نظام المصادقة
        self.auth = SolanaAuth(
            network=os.getenv("SOLANA_NETWORK", "devnet")
        )
        
        # تهيئة نظام التخزين
        self.storage = IPFSStorageManager(
            ipfs_host=os.getenv("IPFS_HOST", "/ip4/127.0.0.1/tcp/5001")
        )
        
        # تهيئة المضغوط
        self.compressor = QuantumInspiredCompressor(
            compression_ratio=float(os.getenv("COMPRESSION_RATIO", 0.1))
        )
        
        logger.info("✅ تم تهيئة جميع المكونات\n")
    
    def display_system_info(self):
        """عرض معلومات النظام"""
        logger.info("="*70)
        logger.info("📊 معلومات النظام")
        logger.info("="*70)
        
        # معلومات السيرفر
        logger.info("\n🎮 السيرفر:")
        logger.info(f"   • العنوان: http://{os.getenv('SERVER_HOST', '0.0.0.0')}:{os.getenv('SERVER_PORT', 8080)}")
        logger.info(f"   • الدقة: {os.getenv('GAME_RESOLUTION', '1280x720')}")
        logger.info(f"   • FPS: {os.getenv('GAME_FPS', 60)}")
        
        # معلومات الضغط
        logger.info("\n🧮 الضغط الكمي:")
        logger.info(f"   • نسبة الضغط: {os.getenv('COMPRESSION_RATIO', 0.1)}")
        logger.info(f"   • Bitrate (720p@60fps): {self.compressor.calculate_bitrate((1280, 720), 60):.2f} Mbps")
        logger.info(f"   • Bitrate (1080p@60fps): {self.compressor.calculate_bitrate((1920, 1080), 60):.2f} Mbps")
        
        # معلومات Solana
        logger.info("\n⛓️ Solana:")
        logger.info(f"   • الشبكة: {os.getenv('SOLANA_NETWORK', 'devnet')}")
        logger.info(f"   • RPC: {os.getenv('SOLANA_RPC_URL', 'https://api.devnet.solana.com')}")
        
        # معلومات IPFS
        logger.info("\n🌐 IPFS:")
        logger.info(f"   • الحالة: {'متصل ✅' if self.storage.client else 'غير متصل ❌'}")
        logger.info(f"   • العنوان: {os.getenv('IPFS_HOST', '/ip4/127.0.0.1/tcp/5001')}")
        
        logger.info("\n" + "="*70)
    
    def display_usage_info(self):
        """عرض معلومات الاستخدام"""
        logger.info("\n📱 عميل الهاتف:")
        logger.info("   1. افتح mobile_client.html في متصفح الهاتف")
        logger.info("   2. غيّر SERVER_URL إلى عنوان السيرفر الفعلي")
        logger.info("   3. اضغط على 'اتصل' للبدء")
        
        logger.info("\n📡 النقاط النهائية المتاحة:")
        logger.info("   • POST /offer - استقبال عروض WebRTC")
        logger.info("   • GET /stats - إحصائيات الأداء")
        logger.info("   • GET /health - فحص صحة السيرفر")
        
        logger.info("\n🧪 اختبار السيرفر:")
        logger.info("   curl http://localhost:8080/health")
        
        logger.info("\n" + "="*70)
    
    def run(self):
        """تشغيل النظام الكامل"""
        try:
            # التحقق من المتطلبات
            if not self.check_dependencies():
                logger.error("❌ فشل التحقق من المتطلبات")
                return False
            
            # إنشاء مجلد السجلات
            Path("logs").mkdir(exist_ok=True)
            
            # تشغيل IPFS
            self.start_ipfs_daemon()
            
            # تهيئة المكونات
            self.initialize_components()
            
            # عرض معلومات النظام
            self.display_system_info()
            self.display_usage_info()
            
            logger.info("\n🚀 تشغيل السيرفر...\n")
            
            # تشغيل السيرفر
            self.server.run()
            
        except KeyboardInterrupt:
            logger.info("\n\n⛔ إيقاف السيرفر...")
            self.cleanup()
        except Exception as e:
            logger.error(f"\n❌ خطأ: {e}")
            self.cleanup()
            return False
    
    def cleanup(self):
        """تنظيف الموارد"""
        logger.info("🧹 تنظيف الموارد...")
        
        # إيقاف IPFS
        if hasattr(self, 'ipfs_process'):
            try:
                self.ipfs_process.terminate()
                self.ipfs_process.wait(timeout=5)
                logger.info("✅ تم إيقاف IPFS")
            except:
                pass
        
        logger.info("✅ تم الإيقاف بنجاح")


# ============================================================================
# نقطة الدخول الرئيسية
# ============================================================================

if __name__ == "__main__":
    launcher = DePINLauncher()
    launcher.run()
