"""
ipfs_storage.py - إدارة التخزين السحابي اللامركزي

هذا الملف يحتوي على:
1. إدارة الاتصال بـ IPFS
2. رفع ملفات الألعاب
3. تحميل الملفات عند الطلب
4. إنشاء ملفات الوصف (Manifests)
5. إدارة الملفات المخزنة
"""

import json
import os
import logging
from typing import Optional, Dict, List
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class IPFSStorageManager:
    """
    إدارة ملفات الألعاب عبر IPFS
    
    المميزات:
    - رفع الملفات إلى IPFS
    - تحميل الملفات عند الطلب
    - إدارة الملفات المخزنة
    - إنشاء ملفات الوصف
    """
    
    def __init__(self, ipfs_host: str = '/ip4/127.0.0.1/tcp/5001'):
        """
        تهيئة مدير IPFS
        
        Args:
            ipfs_host: عنوان الاتصال بـ IPFS
        """
        self.ipfs_host = ipfs_host
        self.client = None
        self.uploaded_files: Dict[str, dict] = {}
        self.file_cache: Dict[str, dict] = {}
        
        # محاولة الاتصال بـ IPFS
        self._connect()
    
    def _connect(self):
        """محاولة الاتصال بـ IPFS"""
        try:
            import ipfshttpclient
            self.client = ipfshttpclient.connect(self.ipfs_host)
            logger.info(f"✅ متصل بـ IPFS على {self.ipfs_host}")
            
            # اختبار الاتصال
            version = self.client.version()
            logger.info(f"📦 إصدار IPFS: {version.get('Version', 'Unknown')}")
            
        except Exception as e:
            logger.warning(f"⚠️ تعذر الاتصال بـ IPFS: {e}")
            logger.info("💡 تأكد من تشغيل IPFS daemon: ipfs daemon")
            self.client = None
    
    def upload_game_assets(self, folder_path: str) -> Optional[str]:
        """
        رفع ملفات اللعبة إلى IPFS
        
        المراحل:
        1. التحقق من وجود المجلد
        2. حساب حجم الملفات
        3. رفع الملفات
        4. الحصول على CID
        5. تخزين معلومات الملفات
        
        Args:
            folder_path: مسار المجلد المراد رفعه
            
        Returns:
            CID الملف الرئيسي
        """
        if not self.client:
            logger.error("❌ لا يوجد اتصال بـ IPFS")
            return None
        
        if not os.path.exists(folder_path):
            logger.error(f"❌ المجلد غير موجود: {folder_path}")
            return None
        
        try:
            logger.info(f"📤 جاري رفع {folder_path}...")
            
            # حساب حجم الملفات
            total_size = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
            
            logger.info(f"   حجم الملفات: {total_size / (1024*1024):.2f} MB")
            
            # رفع الملفات
            result = self.client.add(folder_path, recursive=True)
            
            # الحصول على CID الرئيسي
            cid = result[-1]['Hash'] if isinstance(result, list) else result['Hash']
            
            # تخزين معلومات الملفات
            file_info = {
                "cid": cid,
                "path": folder_path,
                "size_bytes": total_size,
                "uploaded_at": datetime.now().isoformat(),
                "file_count": len(result) if isinstance(result, list) else 1
            }
            
            self.uploaded_files[cid] = file_info
            
            logger.info(f"✅ تم الرفع! CID: {cid}")
            logger.info(f"   الحجم: {total_size / (1024*1024):.2f} MB")
            logger.info(f"   عدد الملفات: {file_info['file_count']}")
            
            return cid
            
        except Exception as e:
            logger.error(f"❌ خطأ في رفع الملفات: {e}")
            return None
    
    def download_on_demand(self, cid: str, output_path: str) -> bool:
        """
        تحميل الملفات عند الطلب
        
        المراحل:
        1. التحقق من الاتصال
        2. التحقق من الذاكرة المؤقتة
        3. تحميل الملفات
        4. تخزين معلومات التحميل
        
        Args:
            cid: معرف المحتوى (Content ID)
            output_path: مسار الحفظ
            
        Returns:
            True إذا نجح التحميل
        """
        if not self.client:
            logger.error("❌ لا يوجد اتصال بـ IPFS")
            return False
        
        try:
            logger.info(f"📥 جاري تحميل {cid}...")
            
            # التحقق من الذاكرة المؤقتة
            if cid in self.file_cache:
                logger.info(f"💾 الملف موجود في الذاكرة المؤقتة")
                return True
            
            # تحميل الملفات
            self.client.get(cid, target=output_path)
            
            # تخزين معلومات التحميل
            self.file_cache[cid] = {
                "output_path": output_path,
                "downloaded_at": datetime.now().isoformat(),
                "size": self._get_directory_size(output_path)
            }
            
            logger.info(f"✅ تم التحميل إلى {output_path}")
            logger.info(f"   الحجم: {self.file_cache[cid]['size'] / (1024*1024):.2f} MB")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل الملفات: {e}")
            return False
    
    def create_game_manifest(self, game_name: str, assets_cid: str,
                            version: str = "1.0.0",
                            resolution: str = "1280x720@60fps",
                            required_bandwidth: str = "2.76 Mbps") -> Optional[str]:
        """
        إنشاء ملف وصف اللعبة
        
        الملف يحتوي على:
        - اسم اللعبة
        - CID الأصول
        - الإصدار
        - المتطلبات
        
        Args:
            game_name: اسم اللعبة
            assets_cid: CID الأصول
            version: إصدار اللعبة
            resolution: دقة الفيديو
            required_bandwidth: معدل البت المطلوب
            
        Returns:
            CID الملف الوصفي
        """
        if not self.client:
            logger.error("❌ لا يوجد اتصال بـ IPFS")
            return None
        
        try:
            manifest = {
                "name": game_name,
                "assets_cid": assets_cid,
                "version": version,
                "required_bandwidth": required_bandwidth,
                "resolution": resolution,
                "created_at": datetime.now().isoformat(),
                "metadata": {
                    "compression": "QFT-based",
                    "protocol": "WebRTC",
                    "blockchain": "Solana"
                }
            }
            
            # حفظ الملف مؤقتاً
            manifest_file = f"{game_name.lower().replace(' ', '_')}_manifest.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📋 جاري رفع ملف الوصف: {manifest_file}")
            
            # رفع الملف
            result = self.client.add(manifest_file)
            manifest_cid = result['Hash']
            
            # حذف الملف المؤقت
            os.remove(manifest_file)
            
            logger.info(f"✅ تم إنشاء ملف الوصف! CID: {manifest_cid}")
            
            return manifest_cid
            
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء ملف الوصف: {e}")
            return None
    
    def pin_file(self, cid: str) -> bool:
        """
        تثبيت ملف لضمان عدم حذفه
        
        Args:
            cid: معرف المحتوى
            
        Returns:
            True إذا نجح التثبيت
        """
        if not self.client:
            return False
        
        try:
            self.client.pin.add(cid)
            logger.info(f"📌 تم تثبيت الملف: {cid}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في تثبيت الملف: {e}")
            return False
    
    def unpin_file(self, cid: str) -> bool:
        """
        إلغاء تثبيت ملف
        
        Args:
            cid: معرف المحتوى
            
        Returns:
            True إذا نجح الإلغاء
        """
        if not self.client:
            return False
        
        try:
            self.client.pin.rm(cid)
            logger.info(f"📍 تم إلغاء تثبيت الملف: {cid}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في إلغاء تثبيت الملف: {e}")
            return False
    
    def get_file_info(self, cid: str) -> Optional[Dict]:
        """الحصول على معلومات الملف"""
        try:
            if self.client:
                stat = self.client.files.stat(f"/ipfs/{cid}")
                return {
                    "cid": cid,
                    "size": stat.get('Size', 0),
                    "type": stat.get('Type', 'unknown'),
                    "retrieved_at": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على معلومات الملف: {e}")
        
        return None
    
    def _get_directory_size(self, path: str) -> int:
        """حساب حجم المجلد"""
        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        return total_size
    
    def get_stats(self) -> Dict:
        """الحصول على إحصائيات التخزين"""
        total_uploaded = sum(f['size_bytes'] for f in self.uploaded_files.values())
        total_cached = sum(f['size'] for f in self.file_cache.values())
        
        return {
            "connection_status": "connected" if self.client else "disconnected",
            "uploaded_files": len(self.uploaded_files),
            "total_uploaded_bytes": total_uploaded,
            "total_uploaded_mb": total_uploaded / (1024*1024),
            "cached_files": len(self.file_cache),
            "total_cached_bytes": total_cached,
            "total_cached_mb": total_cached / (1024*1024),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# اختبار
# ============================================================================

if __name__ == "__main__":
    import logging
    
    # إعداد logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*60)
    print("📁 اختبار نظام التخزين IPFS")
    print("="*60 + "\n")
    
    # إنشاء مدير التخزين
    storage = IPFSStorageManager()
    
    if storage.client:
        print("✅ الاتصال بـ IPFS نجح\n")
        
        # إنشاء ملف وصف تجريبي
        print("📋 إنشاء ملف وصف اللعبة:")
        manifest_cid = storage.create_game_manifest(
            game_name="Fortnite",
            assets_cid="QmExample123456789",
            version="1.0.0",
            resolution="1280x720@60fps",
            required_bandwidth="2.76 Mbps"
        )
        
        if manifest_cid:
            print(f"   CID: {manifest_cid}\n")
        
        # الإحصائيات
        print("📈 إحصائيات التخزين:")
        stats = storage.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
    
    else:
        print("⚠️ تعذر الاتصال بـ IPFS")
        print("💡 تأكد من تشغيل: ipfs daemon\n")
    
    print("\n" + "="*60)
    print("✅ اكتمل الاختبار!")
    print("="*60 + "\n")
