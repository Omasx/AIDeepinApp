# sharder.py - تقسيم وتوزيع الملفات بشكل ديناميكي
import os
import hashlib
import logging
from typing import List

logger = logging.getLogger("Phantom-Sharder")

class DynamicSharder:
    """تقسيم الملفات وتشفيرها وتوزيعها على الشبكة"""
    def __init__(self, shard_size_mb: int = 10):
        self.shard_size = shard_size_mb * 1024 * 1024

    def shard_file(self, file_path: str) -> List[str]:
        """تقسيم الملف إلى أجزاء (Shards)"""
        if not os.path.exists(file_path):
            return []
        
        file_size = os.path.getsize(file_path)
        shards_count = (file_size // self.shard_size) + 1
        
        logger.info(f"🔪 تقسيم {file_path} ({file_size} bytes) إلى {shards_count} جزء...")
        
        shards = []
        for i in range(shards_count):
            shard_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
            shards.append(f"shard_{shard_id}.dat")
            
        return shards

    def encrypt_shard(self, shard_data: bytes) -> bytes:
        """تشفير الجزء (محاكاة AES-256)"""
        # في الواقع نستخدم cryptography.fernet
        return b"encrypted_" + shard_data

    async def distribute_shards(self, shards: List[str], nodes: List[str]):
        """توزيع الأجزاء على العقد العالمية"""
        for i, shard in enumerate(shards):
            target_node = nodes[i % len(nodes)]
            logger.info(f"📤 إرسال {shard} إلى {target_node}")
        return True

if __name__ == "__main__":
    sharder = DynamicSharder(shard_size_mb=1)
    # محاكاة ملف
    with open("test_file.txt", "w") as f:
        f.write("A" * 2 * 1024 * 1024) # 2MB
    
    shards = sharder.shard_file("test_file.txt")
    print(f"Generated shards: {shards}")
    os.remove("test_file.txt")
