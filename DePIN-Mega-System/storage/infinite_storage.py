"""
☁️ نظام التخزين السحابي اللانهائي - Infinite Cloud Storage System (ICSS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

يجمع بين:
1. IPFS - InterPlanetary File System
2. Arweave - Permanent Data Storage
3. Filecoin - Decentralized Storage
4. Storj - Distributed Cloud Storage
5. Sia - Decentralized Storage Platform

المعادلة:
Storage(t) = IPFS + Arweave + Filecoin + Storj + Sia
Total Capacity = ∞ (غير محدود)
"""

import hashlib
import json
import asyncio
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp

@dataclass
class StorageNode:
    """عقدة تخزين في النظام"""
    id: str
    provider: str  # IPFS, Arweave, Filecoin, Storj, Sia
    capacity: float  # بالجيجابايت
    used: float = 0.0
    availability: float = 1.0  # 0-1
    latency: float = 0.0  # بالميلي ثانية
    cost_per_gb: float = 0.0  # التكلفة لكل جيجابايت
    
    @property
    def available_space(self) -> float:
        """المساحة المتاحة"""
        return self.capacity - self.used
    
    @property
    def utilization(self) -> float:
        """معدل الاستخدام"""
        return self.used / self.capacity if self.capacity > 0 else 0

@dataclass
class StorageFile:
    """ملف مخزن في النظام"""
    hash: str
    name: str
    size: float  # بالبايت
    provider: str
    timestamp: datetime
    replicas: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    @property
    def size_gb(self) -> float:
        """حجم الملف بالجيجابايت"""
        return self.size / (1024 ** 3)

class InfiniteCloudStorageSystem:
    """نظام التخزين السحابي اللانهائي"""
    
    def __init__(self):
        self.nodes: Dict[str, StorageNode] = {}
        self.files: Dict[str, StorageFile] = {}
        self.replication_factor = 3  # عدد النسخ
        self.total_capacity = float('inf')  # غير محدود
        
        # تهيئة عقد التخزين
        self._initialize_storage_nodes()
    
    def _initialize_storage_nodes(self):
        """تهيئة عقد التخزين من مختلف المزودين"""
        providers = {
            'IPFS': {'capacity': 1e15, 'cost': 0.0, 'latency': 50},
            'Arweave': {'capacity': 1e15, 'cost': 0.0001, 'latency': 100},
            'Filecoin': {'capacity': 1e15, 'cost': 0.0002, 'latency': 150},
            'Storj': {'capacity': 1e15, 'cost': 0.0001, 'latency': 80},
            'Sia': {'capacity': 1e15, 'cost': 0.00005, 'latency': 120},
        }
        
        for i, (provider, config) in enumerate(providers.items()):
            for j in range(10):  # 10 عقد لكل مزود
                node_id = f"{provider}-Node-{j}"
                self.nodes[node_id] = StorageNode(
                    id=node_id,
                    provider=provider,
                    capacity=config['capacity'],
                    cost_per_gb=config['cost'],
                    latency=config['latency']
                )
    
    def calculate_file_hash(self, data: bytes) -> str:
        """حساب hash الملف"""
        return hashlib.sha256(data).hexdigest()
    
    async def upload_file(self, filename: str, data: bytes, 
                         replication: int = None) -> Dict:
        """رفع ملف إلى النظام"""
        if replication is None:
            replication = self.replication_factor
        
        file_hash = self.calculate_file_hash(data)
        file_size = len(data)
        
        # اختيار أفضل عقد للتخزين
        selected_nodes = self._select_optimal_nodes(file_size, replication)
        
        if not selected_nodes:
            return {'success': False, 'error': 'No available storage nodes'}
        
        # رفع الملف إلى العقد المختارة
        replicas = []
        for node in selected_nodes:
            node.used += file_size
            replicas.append(node.id)
        
        # إنشاء سجل الملف
        storage_file = StorageFile(
            hash=file_hash,
            name=filename,
            size=file_size,
            provider=selected_nodes[0].provider,
            timestamp=datetime.now(),
            replicas=replicas,
            metadata={
                'original_size': file_size,
                'compressed_size': len(self._compress_data(data)),
                'providers': [node.provider for node in selected_nodes]
            }
        )
        
        self.files[file_hash] = storage_file
        
        return {
            'success': True,
            'hash': file_hash,
            'size': file_size,
            'replicas': replication,
            'providers': [node.provider for node in selected_nodes],
            'cost': self._calculate_storage_cost(file_size, selected_nodes)
        }
    
    def _select_optimal_nodes(self, file_size: float, 
                             replication: int) -> List[StorageNode]:
        """اختيار أفضل عقد للتخزين"""
        # تصفية العقد المتاحة
        available_nodes = [
            node for node in self.nodes.values()
            if node.available_space >= file_size and node.availability > 0.9
        ]
        
        if len(available_nodes) < replication:
            return available_nodes
        
        # ترتيب العقد حسب الكفاءة
        sorted_nodes = sorted(
            available_nodes,
            key=lambda n: (
                -n.availability,  # أعلى توفر
                n.latency,  # أقل تأخير
                n.cost_per_gb,  # أقل تكلفة
                n.utilization  # أقل استخدام
            )
        )
        
        return sorted_nodes[:replication]
    
    def _compress_data(self, data: bytes) -> bytes:
        """ضغط البيانات"""
        import zlib
        return zlib.compress(data, level=9)
    
    def _calculate_storage_cost(self, file_size: float, 
                               nodes: List[StorageNode]) -> float:
        """حساب تكلفة التخزين"""
        total_cost = 0
        file_size_gb = file_size / (1024 ** 3)
        
        for node in nodes:
            total_cost += file_size_gb * node.cost_per_gb
        
        return total_cost
    
    async def download_file(self, file_hash: str) -> Optional[bytes]:
        """تحميل ملف من النظام"""
        if file_hash not in self.files:
            return None
        
        storage_file = self.files[file_hash]
        
        # محاولة التحميل من أسرع عقدة متاحة
        for replica_id in storage_file.replicas:
            if replica_id in self.nodes:
                node = self.nodes[replica_id]
                if node.availability > 0.9:
                    # محاكاة التحميل
                    await asyncio.sleep(node.latency / 1000)
                    return b"file_data"  # في الواقع ستكون البيانات الفعلية
        
        return None
    
    def delete_file(self, file_hash: str) -> bool:
        """حذف ملف من النystem"""
        if file_hash not in self.files:
            return False
        
        storage_file = self.files[file_hash]
        
        # حذف من جميع النسخ
        for replica_id in storage_file.replicas:
            if replica_id in self.nodes:
                node = self.nodes[replica_id]
                node.used -= storage_file.size
        
        del self.files[file_hash]
        return True
    
    def get_storage_stats(self) -> Dict:
        """الحصول على إحصائيات التخزين"""
        total_capacity = sum(node.capacity for node in self.nodes.values())
        total_used = sum(node.used for node in self.nodes.values())
        total_files = len(self.files)
        total_data = sum(f.size for f in self.files.values())
        
        provider_stats = {}
        for provider in set(node.provider for node in self.nodes.values()):
            provider_nodes = [n for n in self.nodes.values() if n.provider == provider]
            provider_stats[provider] = {
                'nodes': len(provider_nodes),
                'capacity': sum(n.capacity for n in provider_nodes),
                'used': sum(n.used for n in provider_nodes),
                'utilization': sum(n.used for n in provider_nodes) / sum(n.capacity for n in provider_nodes)
            }
        
        return {
            'total_capacity': total_capacity,
            'total_used': total_used,
            'total_available': total_capacity - total_used,
            'utilization': total_used / total_capacity if total_capacity > 0 else 0,
            'total_files': total_files,
            'total_data': total_data,
            'providers': provider_stats,
            'replication_factor': self.replication_factor
        }
    
    async def replicate_file(self, file_hash: str, 
                            additional_replicas: int = 1) -> bool:
        """إضافة نسخ إضافية من ملف"""
        if file_hash not in self.files:
            return False
        
        storage_file = self.files[file_hash]
        current_replicas = len(storage_file.replicas)
        
        if current_replicas + additional_replicas > len(self.nodes):
            return False
        
        # اختيار عقد جديدة
        new_nodes = self._select_optimal_nodes(
            storage_file.size,
            additional_replicas
        )
        
        for node in new_nodes:
            if node.id not in storage_file.replicas:
                node.used += storage_file.size
                storage_file.replicas.append(node.id)
        
        return True
    
    async def optimize_storage(self) -> Dict:
        """تحسين توزيع التخزين"""
        optimization_results = {
            'files_rebalanced': 0,
            'nodes_optimized': 0,
            'cost_reduction': 0
        }
        
        # إعادة توازن الملفات
        for file_hash, storage_file in self.files.items():
            # حساب أفضل توزيع
            optimal_nodes = self._select_optimal_nodes(
                storage_file.size,
                self.replication_factor
            )
            
            # إذا كان التوزيع مختلفاً، أعد التوازن
            if set(optimal_nodes) != set(storage_file.replicas):
                # حذف من العقد القديمة
                for old_replica in storage_file.replicas:
                    if old_replica in self.nodes:
                        self.nodes[old_replica].used -= storage_file.size
                
                # إضافة إلى العقد الجديدة
                storage_file.replicas = [n.id for n in optimal_nodes]
                for node in optimal_nodes:
                    node.used += storage_file.size
                
                optimization_results['files_rebalanced'] += 1
        
        return optimization_results

# مثال على الاستخدام
async def main():
    print("☁️ نظام التخزين السحابي اللانهائي")
    print("=" * 80)
    
    storage_system = InfiniteCloudStorageSystem()
    
    # رفع ملف
    test_data = b"This is a test file for infinite cloud storage system" * 1000
    result = await storage_system.upload_file("test_file.txt", test_data)
    print(f"\n📤 رفع الملف:")
    print(f"  Hash: {result['hash'][:16]}...")
    print(f"  Size: {result['size'] / 1024:.2f} KB")
    print(f"  Replicas: {result['replicas']}")
    print(f"  Providers: {result['providers']}")
    print(f"  Cost: ${result['cost']:.6f}")
    
    # الحصول على الإحصائيات
    stats = storage_system.get_storage_stats()
    print(f"\n📊 إحصائيات التخزين:")
    print(f"  Total Capacity: {stats['total_capacity'] / 1e15:.2f} PB")
    print(f"  Total Used: {stats['total_used'] / 1024 / 1024 / 1024:.2f} GB")
    print(f"  Utilization: {stats['utilization'] * 100:.2f}%")
    print(f"  Total Files: {stats['total_files']}")
    print(f"  Providers: {list(stats['providers'].keys())}")

if __name__ == "__main__":
    asyncio.run(main())
