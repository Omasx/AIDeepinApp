"""
test_system.py - اختبار شامل لجميع مكونات النظام

هذا الملف يقوم بـ:
1. اختبار محاكاة QFT
2. اختبار نظام المصادقة Solana
3. اختبار نظام التخزين IPFS
4. اختبار السيرفر الرئيسي
"""

import sys
import logging
from pathlib import Path

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemTester:
    """فئة اختبار النظام الشامل"""
    
    def __init__(self):
        """تهيئة المختبر"""
        self.results = {
            "quantum_compression": None,
            "solana_auth": None,
            "ipfs_storage": None,
            "game_server": None
        }
    
    def test_quantum_compression(self) -> bool:
        """اختبار محاكاة QFT"""
        try:
            logger.info("\n" + "="*70)
            logger.info("🧮 اختبار محاكاة QFT")
            logger.info("="*70)
            
            from quantum_compression import QuantumInspiredCompressor
            import numpy as np
            
            # إنشاء المضغوط
            compressor = QuantumInspiredCompressor(compression_ratio=0.1)
            
            # اختبار حساب معدل البت
            logger.info("\n📊 اختبار حساب معدل البت:")
            bitrate_720p = compressor.calculate_bitrate((1280, 720), 60)
            bitrate_1080p = compressor.calculate_bitrate((1920, 1080), 60)
            
            logger.info(f"   ✅ 720p@60fps: {bitrate_720p:.2f} Mbps")
            logger.info(f"   ✅ 1080p@60fps: {bitrate_1080p:.2f} Mbps")
            
            # اختبار الضغط على إطار
            logger.info("\n🎬 اختبار الضغط على إطار:")
            test_frame = np.random.randint(0, 256, (720, 1280, 3), dtype=np.uint8)
            compressed = compressor.apply_qft_simulation(test_frame)
            
            logger.info(f"   ✅ حجم الإطار الأصلي: {test_frame.nbytes / 1024:.2f} KB")
            logger.info(f"   ✅ حجم الإطار المضغوط: {compressed.nbytes / 1024:.2f} KB")
            
            # اختبار حساب التأخير
            logger.info("\n⏱️ اختبار حساب التأخير:")
            latency = compressor.entanglement_bridge_latency(100)
            logger.info(f"   ✅ التأخير لـ 100km: {latency:.2f} ms")
            
            logger.info("\n✅ اختبار QFT نجح!\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل اختبار QFT: {e}")
            return False
    
    def test_solana_auth(self) -> bool:
        """اختبار نظام المصادقة Solana"""
        try:
            logger.info("="*70)
            logger.info("🔐 اختبار نظام المصادقة Solana")
            logger.info("="*70)
            
            from solana_auth import SolanaAuth
            
            # إنشاء نظام المصادقة
            auth = SolanaAuth(network="devnet")
            
            # اختبار محفظة تجريبية
            test_wallet = "valid_11111111111111111111111111111111"
            
            logger.info("\n🔍 اختبار التحقق من NFT:")
            access = auth.verify_nft_access(test_wallet)
            logger.info(f"   ✅ النتيجة: {'لديه حق الوصول' if access else 'بدون حق الوصول'}")
            
            if access:
                # إنشاء رمز جلسة
                logger.info("\n🎫 اختبار إنشاء رمز جلسة:")
                session = auth.create_session_token(test_wallet, duration_hours=1)
                logger.info(f"   ✅ الرمز: {session['token'][:32]}...")
                
                # التحقق من الرمز
                logger.info("\n✔️ اختبار التحقق من الرمز:")
                is_valid, wallet = auth.verify_session_token(session['token'])
                logger.info(f"   ✅ صحيح: {is_valid}")
            
            # اختبار حساب التكلفة
            logger.info("\n💰 اختبار حساب التكلفة:")
            cost = auth.estimate_bandwidth_cost(300)
            logger.info(f"   ✅ الاستهلاك: {cost['bandwidth_gb_per_month']} GB/شهر")
            logger.info(f"   ✅ التكلفة: {cost['cost_sol_per_month']:.6f} SOL")
            
            logger.info("\n✅ اختبار Solana نجح!\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل اختبار Solana: {e}")
            return False
    
    def test_ipfs_storage(self) -> bool:
        """اختبار نظام التخزين IPFS"""
        try:
            logger.info("="*70)
            logger.info("📁 اختبار نظام التخزين IPFS")
            logger.info("="*70)
            
            from ipfs_storage import IPFSStorageManager
            
            # إنشاء مدير التخزين
            storage = IPFSStorageManager()
            
            if storage.client:
                logger.info("\n✅ الاتصال بـ IPFS نجح")
                
                # اختبار إنشاء ملف وصف
                logger.info("\n📋 اختبار إنشاء ملف وصف:")
                manifest_cid = storage.create_game_manifest(
                    game_name="Fortnite",
                    assets_cid="QmExample123456789",
                    version="1.0.0"
                )
                
                if manifest_cid:
                    logger.info(f"   ✅ CID: {manifest_cid}")
                
                # الإحصائيات
                logger.info("\n📈 إحصائيات التخزين:")
                stats = storage.get_stats()
                logger.info(f"   ✅ الملفات المرفوعة: {stats['uploaded_files']}")
                logger.info(f"   ✅ الملفات المخزنة: {stats['cached_files']}")
                
                logger.info("\n✅ اختبار IPFS نجح!\n")
                return True
            else:
                logger.warning("\n⚠️ تعذر الاتصال بـ IPFS")
                logger.info("💡 تأكد من تشغيل: ipfs daemon\n")
                return False
                
        except Exception as e:
            logger.error(f"❌ فشل اختبار IPFS: {e}")
            return False
    
    def test_game_server(self) -> bool:
        """اختبار السيرفر الرئيسي"""
        try:
            logger.info("="*70)
            logger.info("🎮 اختبار السيرفر الرئيسي")
            logger.info("="*70)
            
            from depin_game_server import DePINGameServer, GameCaptureTrack
            
            # إنشاء السيرفر
            logger.info("\n🔧 تهيئة السيرفر:")
            server = DePINGameServer(host="0.0.0.0", port=8080)
            logger.info("   ✅ تم تهيئة السيرفر")
            
            # اختبار مسار التقاط الشاشة
            logger.info("\n🎬 اختبار مسار التقاط الشاشة:")
            track = GameCaptureTrack(resolution=(1280, 720), fps=60)
            logger.info("   ✅ تم تهيئة مسار التقاط الشاشة")
            
            logger.info("\n✅ اختبار السيرفر نجح!\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل اختبار السيرفر: {e}")
            return False
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        logger.info("\n" + "="*70)
        logger.info("🧪 بدء الاختبارات الشاملة للنظام")
        logger.info("="*70)
        
        # تشغيل الاختبارات
        self.results["quantum_compression"] = self.test_quantum_compression()
        self.results["solana_auth"] = self.test_solana_auth()
        self.results["ipfs_storage"] = self.test_ipfs_storage()
        self.results["game_server"] = self.test_game_server()
        
        # عرض النتائج
        self.print_results()
    
    def print_results(self):
        """طباعة نتائج الاختبارات"""
        logger.info("="*70)
        logger.info("📊 نتائج الاختبارات")
        logger.info("="*70)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.results.items():
            status = "✅ نجح" if result else "❌ فشل"
            logger.info(f"   {test_name}: {status}")
            
            if result:
                passed += 1
            else:
                failed += 1
        
        logger.info("\n" + "="*70)
        logger.info(f"📈 الملخص: {passed} نجح، {failed} فشل")
        logger.info("="*70 + "\n")
        
        if failed == 0:
            logger.info("🎉 جميع الاختبارات نجحت!")
            return 0
        else:
            logger.error(f"⚠️ {failed} اختبار فشل")
            return 1


# ============================================================================
# نقطة الدخول الرئيسية
# ============================================================================

if __name__ == "__main__":
    tester = SystemTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
