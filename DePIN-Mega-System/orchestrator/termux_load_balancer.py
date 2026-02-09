"""
⚖️ Termux Load Balancer - موازن الأحمال الخفيف الوزن
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

سكريبت Python خفيف الوزن يعمل في Termux لمراقبة الشبكات واختيار الأسرع
"""

import asyncio
import time
import socket
import subprocess
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import os
import sys

@dataclass
class NetworkMetrics:
    """مقاييس الشبكة"""
    network_name: str
    latency_ms: float = 0.0
    jitter_ms: float = 0.0
    packet_loss_percent: float = 0.0
    bandwidth_mbps: float = 0.0
    uptime_percent: float = 100.0
    last_check: datetime = field(default_factory=datetime.now)
    consecutive_failures: int = 0
    score: float = 0.0
    
    def calculate_score(self) -> float:
        """حساب درجة الأداء (0-100)"""
        # الأوزان
        latency_weight = 0.35
        jitter_weight = 0.20
        packet_loss_weight = 0.25
        uptime_weight = 0.20
        
        # تطبيع القيم
        latency_score = max(0, 100 - (self.latency_ms / 100 * 100))
        jitter_score = max(0, 100 - (self.jitter_ms / 50 * 100))
        packet_loss_score = max(0, 100 - (self.packet_loss_percent * 100))
        uptime_score = self.uptime_percent
        
        # الحساب المرجح
        self.score = (
            latency_score * latency_weight +
            jitter_score * jitter_weight +
            packet_loss_score * packet_loss_weight +
            uptime_score * uptime_weight
        )
        
        return self.score

class TermuxHealthMonitor:
    """مراقب صحة الشبكات في Termux"""
    
    def __init__(self):
        self.networks: Dict[str, Dict] = {
            "akash": {"host": "api.akashnet.net", "port": 443},
            "render": {"host": "api.render.com", "port": 443},
            "golem": {"host": "api.golem.network", "port": 443},
            "iexec": {"host": "api.iexec.network", "port": 443},
            "bittensor": {"host": "api.bittensor.com", "port": 443},
            "petals": {"host": "api.petals.dev", "port": 443},
        }
        self.metrics: Dict[str, NetworkMetrics] = {}
        self.history: List[Dict] = []
        self.check_interval = 30  # ثانية
        self.is_running = False
    
    async def ping_host(self, host: str, timeout: int = 5) -> Tuple[bool, float]:
        """اختبار ping للمضيف"""
        try:
            start_time = time.time()
            
            # محاولة الاتصال
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, 443))
            latency = (time.time() - start_time) * 1000
            
            sock.close()
            
            return result == 0, latency
        except Exception as e:
            return False, 0.0
    
    async def measure_latency(self, network_name: str, host: str, samples: int = 3) -> Tuple[float, float]:
        """قياس زمن الاستجابة والتشتت"""
        latencies = []
        
        for _ in range(samples):
            success, latency = await self.ping_host(host)
            if success:
                latencies.append(latency)
            await asyncio.sleep(0.1)
        
        if not latencies:
            return 0.0, 0.0
        
        avg_latency = sum(latencies) / len(latencies)
        
        # حساب الانحراف المعياري (jitter)
        variance = sum((x - avg_latency) ** 2 for x in latencies) / len(latencies)
        jitter = variance ** 0.5
        
        return avg_latency, jitter
    
    async def check_network_health(self, network_name: str, config: Dict):
        """فحص صحة الشبكة"""
        host = config["host"]
        
        # قياس الزمن
        latency, jitter = await self.measure_latency(network_name, host)
        
        # قياس packet loss (محاكاة)
        success, _ = await self.ping_host(host)
        packet_loss = 0.0 if success else 5.0
        
        # تحديث المقاييس
        if network_name not in self.metrics:
            self.metrics[network_name] = NetworkMetrics(network_name=network_name)
        
        metrics = self.metrics[network_name]
        
        if success:
            metrics.latency_ms = latency
            metrics.jitter_ms = jitter
            metrics.packet_loss_percent = packet_loss
            metrics.consecutive_failures = 0
            metrics.uptime_percent = min(100, metrics.uptime_percent + 1)
        else:
            metrics.consecutive_failures += 1
            metrics.uptime_percent = max(0, metrics.uptime_percent - 5)
        
        metrics.last_check = datetime.now()
        metrics.calculate_score()
    
    async def monitor_all_networks(self):
        """مراقبة جميع الشبكات"""
        self.is_running = True
        
        print("🌐 Termux Load Balancer - بدء المراقبة")
        print("=" * 80)
        
        while self.is_running:
            try:
                # فحص جميع الشبكات بالتوازي
                tasks = [
                    self.check_network_health(name, config)
                    for name, config in self.networks.items()
                ]
                
                await asyncio.gather(*tasks)
                
                # حفظ السجل
                self._record_history()
                
                # عرض النتائج
                self._display_status()
                
                await asyncio.sleep(self.check_interval)
            
            except KeyboardInterrupt:
                print("\n\n⛔ إيقاف المراقبة...")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ خطأ في المراقبة: {e}")
                await asyncio.sleep(self.check_interval)
    
    def _record_history(self):
        """حفظ السجل"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "networks": {
                name: {
                    "latency_ms": metrics.latency_ms,
                    "jitter_ms": metrics.jitter_ms,
                    "packet_loss_percent": metrics.packet_loss_percent,
                    "score": metrics.score,
                    "uptime_percent": metrics.uptime_percent
                }
                for name, metrics in self.metrics.items()
            }
        }
        self.history.append(record)
        
        # الاحتفاظ بآخر 1000 سجل فقط
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
    
    def _display_status(self):
        """عرض حالة الشبكات"""
        # مسح الشاشة
        os.system("clear" if os.name != "nt" else "cls")
        
        print("⚖️ Termux Load Balancer - حالة الشبكات")
        print("=" * 80)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # ترتيب حسب الدرجة
        sorted_networks = sorted(
            self.metrics.items(),
            key=lambda x: x[1].score,
            reverse=True
        )
        
        # عرض الجدول
        print(f"{'الشبكة':<15} {'الزمن':<10} {'التشتت':<10} {'الفقد':<10} {'الدرجة':<10} {'الحالة':<10}")
        print("-" * 80)
        
        for i, (name, metrics) in enumerate(sorted_networks, 1):
            status_emoji = "✅" if metrics.score > 70 else "⚠️" if metrics.score > 40 else "❌"
            
            print(
                f"{name:<15} "
                f"{metrics.latency_ms:>8.1f}ms "
                f"{metrics.jitter_ms:>8.1f}ms "
                f"{metrics.packet_loss_percent:>8.1f}% "
                f"{metrics.score:>8.1f}/100 "
                f"{status_emoji:<10}"
            )
        
        # أفضل شبكة
        best_network = sorted_networks[0] if sorted_networks else None
        if best_network:
            print()
            print(f"🏆 أفضل شبكة: {best_network[0].upper()}")
            print(f"   الدرجة: {best_network[1].score:.1f}/100")
            print(f"   الزمن: {best_network[1].latency_ms:.1f}ms")
            print(f"   الموثوقية: {best_network[1].uptime_percent:.1f}%")
        
        # الإحصائيات
        print()
        print("📊 الإحصائيات:")
        print(f"  عدد الشبكات: {len(self.metrics)}")
        print(f"  متوسط الدرجة: {sum(m.score for m in self.metrics.values()) / len(self.metrics):.1f}/100")
        print(f"  السجلات المحفوظة: {len(self.history)}")
    
    def get_best_network(self) -> Optional[str]:
        """الحصول على أفضل شبكة"""
        if not self.metrics:
            return None
        
        best = max(self.metrics.items(), key=lambda x: x[1].score)
        return best[0]
    
    def get_network_recommendation(self, task_type: str) -> str:
        """الحصول على توصية الشبكة"""
        if not self.metrics:
            return "unknown"
        
        # التوصيات حسب نوع المهمة
        recommendations = {
            "gpu": ["render", "golem"],
            "ai": ["bittensor", "petals"],
            "compute": ["akash", "iexec"],
            "storage": ["akash", "iexec"],
        }
        
        preferred = recommendations.get(task_type, list(self.metrics.keys()))
        
        # اختيار الأفضل من المفضلة
        best_preferred = None
        best_score = -1
        
        for net in preferred:
            if net in self.metrics and self.metrics[net].score > best_score:
                best_score = self.metrics[net].score
                best_preferred = net
        
        return best_preferred or self.get_best_network() or "unknown"
    
    def export_metrics(self, filename: str = "network_metrics.json"):
        """تصدير المقاييس"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                name: {
                    "latency_ms": metrics.latency_ms,
                    "jitter_ms": metrics.jitter_ms,
                    "packet_loss_percent": metrics.packet_loss_percent,
                    "score": metrics.score,
                    "uptime_percent": metrics.uptime_percent,
                    "consecutive_failures": metrics.consecutive_failures
                }
                for name, metrics in self.metrics.items()
            },
            "best_network": self.get_best_network(),
            "history_count": len(self.history)
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 تم تصدير المقاييس إلى {filename}")

class TermuxLoadBalancer:
    """موازن الأحمال الرئيسي"""
    
    def __init__(self):
        self.monitor = TermuxHealthMonitor()
        self.task_queue: List[Dict] = []
    
    async def start(self):
        """بدء موازن الأحمال"""
        print("🚀 بدء Termux Load Balancer...")
        
        # بدء المراقبة
        await self.monitor.monitor_all_networks()
    
    def submit_task(self, task_type: str, task_data: Dict) -> str:
        """إرسال مهمة"""
        best_network = self.monitor.get_network_recommendation(task_type)
        
        task = {
            "id": f"task-{int(time.time() * 1000)}",
            "type": task_type,
            "network": best_network,
            "data": task_data,
            "submitted_at": datetime.now().isoformat()
        }
        
        self.task_queue.append(task)
        
        print(f"📤 تم إرسال المهمة {task['id']} إلى {best_network}")
        return task["id"]
    
    def get_status(self) -> Dict:
        """الحصول على الحالة"""
        return {
            "best_network": self.monitor.get_best_network(),
            "metrics": {
                name: {
                    "score": metrics.score,
                    "latency_ms": metrics.latency_ms
                }
                for name, metrics in self.monitor.metrics.items()
            },
            "pending_tasks": len(self.task_queue)
        }

# مثال على الاستخدام
async def main():
    print("⚖️ Termux Load Balancer - مثال على الاستخدام")
    print("=" * 80)
    
    balancer = TermuxLoadBalancer()
    
    # بدء المراقبة
    try:
        await balancer.start()
    except KeyboardInterrupt:
        print("\n\n✅ تم إيقاف موازن الأحمال")
        
        # تصدير المقاييس
        balancer.monitor.export_metrics()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ تم الإيقاف")
