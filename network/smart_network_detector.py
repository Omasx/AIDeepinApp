"""
🌐 نظام اكتشاف الشبكات الذكي - Smart Network Detection System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نظام ذكي لاكتشاف الشبكات المتاحة والاتصال بشبكات DePIN البديلة عند انقطاع الإنترنت
"""

import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math
from datetime import datetime

class NetworkType(Enum):
    """أنواع الشبكات"""
    INTERNET = "internet"
    WIFI = "wifi"
    CELLULAR = "cellular"
    BLUETOOTH = "bluetooth"
    DEPIN = "depin"
    MESH = "mesh"
    SATELLITE = "satellite"

class ConnectionQuality(Enum):
    """جودة الاتصال"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    OFFLINE = "offline"

@dataclass
class NetworkNode:
    """عقدة شبكة"""
    id: str
    name: str
    type: NetworkType
    signal_strength: float  # 0-100
    latency: float  # بالميلي ثانية
    bandwidth: float  # بـ Mbps
    location: Tuple[float, float]  # (latitude, longitude)
    distance: float = 0.0  # المسافة من الجهاز الحالي
    quality: ConnectionQuality = ConnectionQuality.OFFLINE
    is_available: bool = True
    last_seen: datetime = field(default_factory=datetime.now)
    
    def calculate_quality(self) -> ConnectionQuality:
        """حساب جودة الاتصال"""
        score = (self.signal_strength * 0.4 + 
                (100 - min(self.latency, 100)) * 0.3 +
                min(self.bandwidth / 100, 1) * 100 * 0.3)
        
        if score >= 80:
            return ConnectionQuality.EXCELLENT
        elif score >= 60:
            return ConnectionQuality.GOOD
        elif score >= 40:
            return ConnectionQuality.FAIR
        elif score >= 20:
            return ConnectionQuality.POOR
        else:
            return ConnectionQuality.OFFLINE

@dataclass
class OfflineModeConfig:
    """إعدادات وضع بدون إنترنت"""
    enabled: bool = True
    auto_connect: bool = True
    prefer_depin: bool = True
    max_distance: float = 5000.0  # بالمتر
    min_signal_strength: float = 20.0
    timeout: float = 30.0  # ثانية
    retry_interval: float = 5.0  # ثانية

class SmartNetworkDetector:
    """نظام اكتشاف الشبكات الذكي"""
    
    def __init__(self, config: OfflineModeConfig = None):
        self.config = config or OfflineModeConfig()
        self.available_networks: Dict[str, NetworkNode] = {}
        self.current_network: Optional[NetworkNode] = None
        self.user_location: Tuple[float, float] = (0.0, 0.0)
        self.connection_history: List[Dict] = []
        self._initialize_depin_nodes()
    
    def _initialize_depin_nodes(self):
        """تهيئة عقد DePIN المعروفة"""
        # عقد DePIN الرئيسية حول العالم
        depin_nodes = [
            # آسيا
            NetworkNode(
                id="depin-asia-1",
                name="DePIN Asia Hub",
                type=NetworkType.DEPIN,
                signal_strength=95,
                latency=15,
                bandwidth=1000,
                location=(35.6762, 139.6503)  # طوكيو
            ),
            NetworkNode(
                id="depin-asia-2",
                name="DePIN Middle East Hub",
                type=NetworkType.DEPIN,
                signal_strength=90,
                latency=20,
                bandwidth=800,
                location=(24.4539, 54.3773)  # دبي
            ),
            # أوروبا
            NetworkNode(
                id="depin-eu-1",
                name="DePIN Europe Hub",
                type=NetworkType.DEPIN,
                signal_strength=92,
                latency=10,
                bandwidth=1200,
                location=(48.8566, 2.3522)  # باريس
            ),
            # أمريكا
            NetworkNode(
                id="depin-us-1",
                name="DePIN USA Hub",
                type=NetworkType.DEPIN,
                signal_strength=93,
                latency=12,
                bandwidth=1100,
                location=(40.7128, -74.0060)  # نيويورك
            ),
        ]
        
        for node in depin_nodes:
            self.available_networks[node.id] = node
    
    def calculate_distance(self, loc1: Tuple[float, float], 
                          loc2: Tuple[float, float]) -> float:
        """حساب المسافة بين نقطتين (بالمتر)"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
        # صيغة Haversine
        R = 6371000  # نصف قطر الأرض بالمتر
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) ** 2)
        
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    async def scan_networks(self, user_location: Tuple[float, float]) -> List[NetworkNode]:
        """مسح الشبكات المتاحة"""
        self.user_location = user_location
        available = []
        
        for node in self.available_networks.values():
            # حساب المسافة
            node.distance = self.calculate_distance(user_location, node.location)
            
            # التحقق من التوفر
            if (node.distance <= self.config.max_distance and
                node.signal_strength >= self.config.min_signal_strength and
                node.is_available):
                
                # حساب جودة الاتصال
                node.quality = node.calculate_quality()
                available.append(node)
        
        # ترتيب حسب الجودة والمسافة
        available.sort(key=lambda n: (-n.signal_strength, n.distance))
        
        return available
    
    async def connect_to_best_network(self, 
                                     user_location: Tuple[float, float],
                                     prefer_type: NetworkType = None) -> Optional[NetworkNode]:
        """الاتصال بأفضل شبكة متاحة"""
        available = await self.scan_networks(user_location)
        
        if not available:
            return None
        
        # الأولوية للشبكات المفضلة
        if self.config.prefer_depin:
            depin_networks = [n for n in available if n.type == NetworkType.DEPIN]
            if depin_networks:
                best_network = depin_networks[0]
            else:
                best_network = available[0]
        else:
            best_network = available[0]
        
        # الاتصال
        self.current_network = best_network
        self.connection_history.append({
            'timestamp': datetime.now(),
            'network_id': best_network.id,
            'network_name': best_network.name,
            'signal_strength': best_network.signal_strength,
            'latency': best_network.latency
        })
        
        return best_network
    
    async def auto_reconnect(self, user_location: Tuple[float, float]):
        """إعادة الاتصال التلقائي"""
        while self.config.auto_connect:
            try:
                network = await self.connect_to_best_network(user_location)
                
                if network:
                    print(f"✅ متصل بـ: {network.name}")
                    await asyncio.sleep(self.config.retry_interval)
                else:
                    print("❌ لا توجد شبكات متاحة")
                    await asyncio.sleep(self.config.retry_interval)
                    
            except Exception as e:
                print(f"❌ خطأ في الاتصال: {e}")
                await asyncio.sleep(self.config.retry_interval)
    
    def get_network_status(self) -> Dict:
        """الحصول على حالة الشبكة"""
        return {
            'current_network': {
                'id': self.current_network.id if self.current_network else None,
                'name': self.current_network.name if self.current_network else 'غير متصل',
                'type': self.current_network.type.value if self.current_network else None,
                'signal_strength': self.current_network.signal_strength if self.current_network else 0,
                'latency': self.current_network.latency if self.current_network else 0,
                'quality': self.current_network.quality.value if self.current_network else 'offline'
            },
            'available_networks': [
                {
                    'id': n.id,
                    'name': n.name,
                    'type': n.type.value,
                    'signal_strength': n.signal_strength,
                    'distance': round(n.distance / 1000, 2),  # بالكيلومتر
                    'quality': n.calculate_quality().value
                }
                for n in sorted(self.available_networks.values(), 
                               key=lambda n: -n.signal_strength)[:5]
            ],
            'user_location': self.user_location,
            'offline_mode_enabled': self.config.enabled,
            'auto_connect_enabled': self.config.auto_connect
        }
    
    async def get_network_recommendations(self, 
                                         user_location: Tuple[float, float]) -> List[Dict]:
        """الحصول على توصيات الشبكة"""
        available = await self.scan_networks(user_location)
        
        recommendations = []
        for i, network in enumerate(available[:3], 1):
            recommendations.append({
                'rank': i,
                'name': network.name,
                'type': network.type.value,
                'signal_strength': network.signal_strength,
                'latency': network.latency,
                'distance_km': round(network.distance / 1000, 2),
                'quality': network.quality.value,
                'reason': self._get_recommendation_reason(network, i)
            })
        
        return recommendations
    
    def _get_recommendation_reason(self, network: NetworkNode, rank: int) -> str:
        """الحصول على سبب التوصية"""
        if rank == 1:
            return "أفضل اتصال متاح"
        elif network.type == NetworkType.DEPIN:
            return "شبكة DePIN موثوقة"
        elif network.signal_strength > 80:
            return "إشارة قوية جداً"
        else:
            return "خيار بديل جيد"

# مثال على الاستخدام
async def main():
    print("🌐 نظام اكتشاف الشبكات الذكي")
    print("=" * 80)
    
    # تهيئة النظام
    config = OfflineModeConfig(
        enabled=True,
        auto_connect=True,
        prefer_depin=True
    )
    
    detector = SmartNetworkDetector(config)
    
    # موقع المستخدم (مثال: الرياض)
    user_location = (24.7136, 46.6753)
    
    # مسح الشبكات
    print("\n📡 مسح الشبكات المتاحة...")
    available = await detector.scan_networks(user_location)
    
    print(f"\n✅ عدد الشبكات المتاحة: {len(available)}")
    for network in available[:3]:
        print(f"  • {network.name}")
        print(f"    - الإشارة: {network.signal_strength}%")
        print(f"    - التأخير: {network.latency}ms")
        print(f"    - المسافة: {round(network.distance/1000, 2)} km")
    
    # الاتصال بأفضل شبكة
    print("\n🔌 الاتصال بأفضل شبكة...")
    best_network = await detector.connect_to_best_network(user_location)
    
    if best_network:
        print(f"✅ متصل بـ: {best_network.name}")
    
    # الحصول على التوصيات
    print("\n💡 توصيات الشبكة:")
    recommendations = await detector.get_network_recommendations(user_location)
    for rec in recommendations:
        print(f"  {rec['rank']}. {rec['name']}")
        print(f"     - {rec['reason']}")
        print(f"     - الجودة: {rec['quality']}")
    
    # حالة الشبكة
    print("\n📊 حالة الشبكة:")
    status = detector.get_network_status()
    print(f"  الشبكة الحالية: {status['current_network']['name']}")
    print(f"  الإشارة: {status['current_network']['signal_strength']}%")
    print(f"  التأخير: {status['current_network']['latency']}ms")

if __name__ == "__main__":
    asyncio.run(main())
