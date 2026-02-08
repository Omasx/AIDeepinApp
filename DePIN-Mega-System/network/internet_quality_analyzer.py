"""
📊 محلل جودة الإنترنت - Internet Quality Analyzer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نظام شامل لتقييم وتحليل جودة الإنترنت والشبكات
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics

class SpeedCategory(Enum):
    """فئات السرعة"""
    ULTRA_FAST = "ultra_fast"      # 100+ Mbps
    VERY_FAST = "very_fast"        # 50-100 Mbps
    FAST = "fast"                  # 20-50 Mbps
    MODERATE = "moderate"          # 5-20 Mbps
    SLOW = "slow"                  # 1-5 Mbps
    VERY_SLOW = "very_slow"        # <1 Mbps

class LatencyLevel(Enum):
    """مستويات التأخير"""
    EXCELLENT = "excellent"        # <10 ms
    VERY_GOOD = "very_good"        # 10-20 ms
    GOOD = "good"                  # 20-50 ms
    FAIR = "fair"                  # 50-100 ms
    POOR = "poor"                  # 100-200 ms
    VERY_POOR = "very_poor"        # >200 ms

@dataclass
class SpeedTest:
    """نتيجة اختبار السرعة"""
    download_mbps: float
    upload_mbps: float
    latency_ms: float
    jitter_ms: float
    packet_loss_percent: float
    timestamp: str

@dataclass
class NetworkQualityScore:
    """درجة جودة الشبكة"""
    overall_score: float  # 0-100
    speed_score: float
    latency_score: float
    stability_score: float
    security_score: float
    reliability_score: float
    rating: str  # ممتاز، جيد، مقبول، ضعيف

class InternetQualityAnalyzer:
    """محلل جودة الإنترنت"""
    
    def __init__(self):
        self.speed_tests: List[SpeedTest] = []
        self.network_history: List[Dict] = []
    
    def categorize_speed(self, speed_mbps: float) -> SpeedCategory:
        """تصنيف السرعة"""
        if speed_mbps >= 100:
            return SpeedCategory.ULTRA_FAST
        elif speed_mbps >= 50:
            return SpeedCategory.VERY_FAST
        elif speed_mbps >= 20:
            return SpeedCategory.FAST
        elif speed_mbps >= 5:
            return SpeedCategory.MODERATE
        elif speed_mbps >= 1:
            return SpeedCategory.SLOW
        else:
            return SpeedCategory.VERY_SLOW
    
    def categorize_latency(self, latency_ms: float) -> LatencyLevel:
        """تصنيف التأخير"""
        if latency_ms < 10:
            return LatencyLevel.EXCELLENT
        elif latency_ms < 20:
            return LatencyLevel.VERY_GOOD
        elif latency_ms < 50:
            return LatencyLevel.GOOD
        elif latency_ms < 100:
            return LatencyLevel.FAIR
        elif latency_ms < 200:
            return LatencyLevel.POOR
        else:
            return LatencyLevel.VERY_POOR
    
    def calculate_speed_score(self, download_mbps: float, upload_mbps: float) -> float:
        """حساب درجة السرعة (0-100)"""
        # المعايير المثالية
        ideal_download = 100  # Mbps
        ideal_upload = 50     # Mbps
        
        download_score = min((download_mbps / ideal_download) * 100, 100)
        upload_score = min((upload_mbps / ideal_upload) * 100, 100)
        
        return (download_score * 0.7 + upload_score * 0.3)
    
    def calculate_latency_score(self, latency_ms: float) -> float:
        """حساب درجة التأخير (0-100)"""
        # التأخير المثالي: 10ms
        if latency_ms <= 10:
            return 100
        elif latency_ms <= 50:
            return 100 - ((latency_ms - 10) / 40 * 25)
        elif latency_ms <= 100:
            return 75 - ((latency_ms - 50) / 50 * 25)
        elif latency_ms <= 200:
            return 50 - ((latency_ms - 100) / 100 * 30)
        else:
            return max(0, 20 - ((latency_ms - 200) / 100 * 20))
    
    def calculate_stability_score(self, jitter_ms: float, packet_loss_percent: float) -> float:
        """حساب درجة الاستقرار (0-100)"""
        # جودة مثالية: jitter < 5ms، packet loss < 0.1%
        jitter_score = max(0, 100 - (jitter_ms * 5))
        packet_loss_score = max(0, 100 - (packet_loss_percent * 100))
        
        return (jitter_score * 0.5 + packet_loss_score * 0.5)
    
    def calculate_overall_score(self, test: SpeedTest) -> NetworkQualityScore:
        """حساب الدرجة الإجمالية"""
        speed_score = self.calculate_speed_score(test.download_mbps, test.upload_mbps)
        latency_score = self.calculate_latency_score(test.latency_ms)
        stability_score = self.calculate_stability_score(test.jitter_ms, test.packet_loss_percent)
        
        # درجات ثابتة للأمان والموثوقية (يمكن تحديثها لاحقاً)
        security_score = 75.0
        reliability_score = 80.0
        
        # حساب الدرجة الإجمالية
        overall_score = (
            speed_score * 0.35 +
            latency_score * 0.25 +
            stability_score * 0.20 +
            security_score * 0.10 +
            reliability_score * 0.10
        )
        
        # تحديد التقييم
        if overall_score >= 80:
            rating = "ممتاز 🌟"
        elif overall_score >= 60:
            rating = "جيد ✅"
        elif overall_score >= 40:
            rating = "مقبول ⚠️"
        else:
            rating = "ضعيف ❌"
        
        return NetworkQualityScore(
            overall_score=round(overall_score, 1),
            speed_score=round(speed_score, 1),
            latency_score=round(latency_score, 1),
            stability_score=round(stability_score, 1),
            security_score=round(security_score, 1),
            reliability_score=round(reliability_score, 1),
            rating=rating
        )
    
    def add_speed_test(self, test: SpeedTest):
        """إضافة نتيجة اختبار سرعة"""
        self.speed_tests.append(test)
        
        # حساب الدرجة
        score = self.calculate_overall_score(test)
        
        self.network_history.append({
            'timestamp': test.timestamp,
            'download_mbps': test.download_mbps,
            'upload_mbps': test.upload_mbps,
            'latency_ms': test.latency_ms,
            'overall_score': score.overall_score,
            'rating': score.rating
        })
    
    def get_average_metrics(self) -> Dict:
        """الحصول على متوسط المقاييس"""
        if not self.speed_tests:
            return {}
        
        downloads = [t.download_mbps for t in self.speed_tests]
        uploads = [t.upload_mbps for t in self.speed_tests]
        latencies = [t.latency_ms for t in self.speed_tests]
        jitters = [t.jitter_ms for t in self.speed_tests]
        packet_losses = [t.packet_loss_percent for t in self.speed_tests]
        
        return {
            'avg_download_mbps': round(statistics.mean(downloads), 2),
            'avg_upload_mbps': round(statistics.mean(uploads), 2),
            'avg_latency_ms': round(statistics.mean(latencies), 2),
            'avg_jitter_ms': round(statistics.mean(jitters), 2),
            'avg_packet_loss_percent': round(statistics.mean(packet_losses), 2),
            'min_download_mbps': min(downloads),
            'max_download_mbps': max(downloads),
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'test_count': len(self.speed_tests)
        }
    
    def get_network_recommendations(self, score: NetworkQualityScore) -> List[str]:
        """الحصول على توصيات تحسين الشبكة"""
        recommendations = []
        
        if score.speed_score < 50:
            recommendations.append("🔴 السرعة منخفضة جداً - جرب شبكة أخرى")
        elif score.speed_score < 70:
            recommendations.append("🟡 السرعة يمكن تحسينها - ابحث عن شبكة أفضل")
        
        if score.latency_score < 50:
            recommendations.append("🔴 التأخير مرتفع - قد تواجه مشاكل في الألعاب والمكالمات")
        elif score.latency_score < 70:
            recommendations.append("🟡 التأخير متوسط - قد تواجه بطء طفيف")
        
        if score.stability_score < 50:
            recommendations.append("🔴 الاتصال غير مستقر - قد تحدث قطع متكررة")
        elif score.stability_score < 70:
            recommendations.append("🟡 الاستقرار يحتاج تحسين - قد تحدث قطع عرضية")
        
        if not recommendations:
            recommendations.append("✅ الاتصال ممتاز - لا توجد مشاكل")
        
        return recommendations
    
    def compare_networks(self, networks: List[Tuple[str, NetworkQualityScore]]) -> List[Dict]:
        """مقارنة عدة شبكات"""
        comparison = []
        
        for name, score in networks:
            comparison.append({
                'name': name,
                'overall_score': score.overall_score,
                'speed_score': score.speed_score,
                'latency_score': score.latency_score,
                'stability_score': score.stability_score,
                'rating': score.rating
            })
        
        # ترتيب حسب الدرجة الإجمالية
        comparison.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return comparison
    
    def get_best_use_case(self, score: NetworkQualityScore) -> List[str]:
        """الحصول على أفضل حالات الاستخدام للشبكة"""
        use_cases = []
        
        if score.speed_score >= 80:
            use_cases.extend(["📥 تحميل الملفات الكبيرة", "🎬 مشاهدة الفيديو 4K"])
        elif score.speed_score >= 60:
            use_cases.extend(["📹 مشاهدة الفيديو HD", "📧 تصفح الويب"])
        else:
            use_cases.append("📱 استخدام وسائل التواصل الاجتماعي")
        
        if score.latency_score >= 80:
            use_cases.extend(["🎮 الألعاب الأونلاين", "📞 المكالمات الفيديو"])
        elif score.latency_score >= 60:
            use_cases.append("💬 المحادثات النصية")
        
        return use_cases

# مثال على الاستخدام
if __name__ == "__main__":
    print("📊 محلل جودة الإنترنت")
    print("=" * 80)
    
    analyzer = InternetQualityAnalyzer()
    
    # اختبار شبكات مختلفة
    networks = [
        ("DePIN Hub - الرياض", SpeedTest(
            download_mbps=95,
            upload_mbps=45,
            latency_ms=15,
            jitter_ms=2,
            packet_loss_percent=0.1,
            timestamp="2026-02-08 10:00:00"
        )),
        ("WiFi عام - مقهى", SpeedTest(
            download_mbps=15,
            upload_mbps=8,
            latency_ms=35,
            jitter_ms=5,
            packet_loss_percent=0.5,
            timestamp="2026-02-08 10:05:00"
        )),
        ("شبكة مجتمع", SpeedTest(
            download_mbps=30,
            upload_mbps=20,
            latency_ms=20,
            jitter_ms=3,
            packet_loss_percent=0.2,
            timestamp="2026-02-08 10:10:00"
        )),
    ]
    
    results = []
    for name, test in networks:
        analyzer.add_speed_test(test)
        score = analyzer.calculate_overall_score(test)
        results.append((name, score))
        
        print(f"\n🌐 {name}")
        print(f"  📥 التحميل: {test.download_mbps} Mbps")
        print(f"  📤 الرفع: {test.upload_mbps} Mbps")
        print(f"  ⏱️  التأخير: {test.latency_ms} ms")
        print(f"  📊 الدرجة الإجمالية: {score.overall_score}/100 {score.rating}")
        
        recommendations = analyzer.get_network_recommendations(score)
        print(f"  💡 التوصيات:")
        for rec in recommendations:
            print(f"     {rec}")
        
        use_cases = analyzer.get_best_use_case(score)
        print(f"  ✅ أفضل الاستخدامات:")
        for use_case in use_cases:
            print(f"     {use_case}")
    
    # مقارنة الشبكات
    print(f"\n📊 مقارنة الشبكات:")
    comparison = analyzer.compare_networks(results)
    for i, net in enumerate(comparison, 1):
        print(f"  {i}. {net['name']}")
        print(f"     - الدرجة: {net['overall_score']}/100 {net['rating']}")
    
    # المتوسطات
    print(f"\n📈 المتوسطات:")
    avg = analyzer.get_average_metrics()
    print(f"  متوسط التحميل: {avg['avg_download_mbps']} Mbps")
    print(f"  متوسط التأخير: {avg['avg_latency_ms']} ms")
    print(f"  عدد الاختبارات: {avg['test_count']}")
