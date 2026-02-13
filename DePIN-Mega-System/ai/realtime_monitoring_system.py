"""
📊 Real-time Monitoring System - نظام المراقبة الفورية
نظام مراقبة فورية متقدم لجميع مكونات الذكاء الاصطناعي

يدعم:
- مراقبة الأداء الفورية
- تحليل الموارد
- تنبيهات الأخطاء
- لوحة التحكم الحية
- تسجيل الأحداث
- التقارير المفصلة
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import json
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """أنواع المقاييس"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    GPU_USAGE = "gpu_usage"
    NETWORK_LATENCY = "network_latency"
    TASK_COMPLETION_TIME = "task_completion_time"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESPONSE_TIME = "response_time"


class AlertLevel(Enum):
    """مستويات التنبيه"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"


@dataclass
class Metric:
    """مقياس"""
    metric_type: MetricType
    value: float
    timestamp: float
    source: str
    unit: str


@dataclass
class Alert:
    """تنبيه"""
    alert_id: str
    level: AlertLevel
    message: str
    timestamp: float
    source: str
    resolved: bool = False


class MetricsCollector:
    """جامع المقاييس"""
    
    def __init__(self, max_history: int = 1000):
        self.metrics: Dict[MetricType, deque] = {
            metric_type: deque(maxlen=max_history)
            for metric_type in MetricType
        }
        self.max_history = max_history
    
    async def collect_metric(self, metric: Metric):
        """جمع مقياس"""
        
        self.metrics[metric.metric_type].append(metric)
        
        logger.debug(f"📊 جمع مقياس: {metric.metric_type.value} = {metric.value} {metric.unit}")
    
    async def get_metric_history(self, metric_type: MetricType, limit: int = 100) -> List[Metric]:
        """الحصول على سجل المقاييس"""
        
        history = list(self.metrics[metric_type])
        return history[-limit:]
    
    async def get_average(self, metric_type: MetricType) -> float:
        """حساب المتوسط"""
        
        metrics = list(self.metrics[metric_type])
        if not metrics:
            return 0.0
        
        values = [m.value for m in metrics]
        return np.mean(values)
    
    async def get_max(self, metric_type: MetricType) -> float:
        """الحصول على القيمة القصوى"""
        
        metrics = list(self.metrics[metric_type])
        if not metrics:
            return 0.0
        
        values = [m.value for m in metrics]
        return np.max(values)
    
    async def get_min(self, metric_type: MetricType) -> float:
        """الحصول على القيمة الدنيا"""
        
        metrics = list(self.metrics[metric_type])
        if not metrics:
            return 0.0
        
        values = [m.value for m in metrics]
        return np.min(values)


class AlertManager:
    """مدير التنبيهات"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[MetricType, Dict] = {
            MetricType.CPU_USAGE: {'warning': 80, 'critical': 95},
            MetricType.MEMORY_USAGE: {'warning': 75, 'critical': 90},
            MetricType.GPU_USAGE: {'warning': 85, 'critical': 98},
            MetricType.ERROR_RATE: {'warning': 0.05, 'critical': 0.1},
            MetricType.RESPONSE_TIME: {'warning': 1000, 'critical': 5000},  # ms
        }
        self.alert_counter = 0
    
    async def check_alert_conditions(self, metric: Metric) -> Optional[Alert]:
        """فحص شروط التنبيه"""
        
        if metric.metric_type not in self.alert_rules:
            return None
        
        rules = self.alert_rules[metric.metric_type]
        
        if metric.value >= rules.get('critical', float('inf')):
            alert = Alert(
                alert_id=f"alert_{self.alert_counter}",
                level=AlertLevel.CRITICAL,
                message=f"قيمة حرجة: {metric.metric_type.value} = {metric.value} {metric.unit}",
                timestamp=metric.timestamp,
                source=metric.source
            )
            self.alert_counter += 1
            return alert
        
        elif metric.value >= rules.get('warning', float('inf')):
            alert = Alert(
                alert_id=f"alert_{self.alert_counter}",
                level=AlertLevel.WARNING,
                message=f"تحذير: {metric.metric_type.value} = {metric.value} {metric.unit}",
                timestamp=metric.timestamp,
                source=metric.source
            )
            self.alert_counter += 1
            return alert
        
        return None
    
    async def add_alert(self, alert: Alert):
        """إضافة تنبيه"""
        
        self.alerts.append(alert)
        
        if alert.level == AlertLevel.CRITICAL:
            logger.critical(f"🚨 {alert.message}")
        elif alert.level == AlertLevel.WARNING:
            logger.warning(f"⚠️ {alert.message}")
        else:
            logger.info(f"ℹ️ {alert.message}")
    
    async def resolve_alert(self, alert_id: str):
        """حل تنبيه"""
        
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"✅ تم حل التنبيه: {alert_id}")
                break
    
    async def get_active_alerts(self) -> List[Alert]:
        """الحصول على التنبيهات النشطة"""
        
        return [a for a in self.alerts if not a.resolved]


class PerformanceAnalyzer:
    """محلل الأداء"""
    
    def __init__(self):
        self.performance_data = {}
        self.bottlenecks = []
    
    async def analyze_performance(self, metrics_collector: MetricsCollector) -> Dict:
        """تحليل الأداء"""
        
        logger.info("📈 جاري تحليل الأداء")
        
        analysis = {
            'cpu': {
                'average': await metrics_collector.get_average(MetricType.CPU_USAGE),
                'max': await metrics_collector.get_max(MetricType.CPU_USAGE),
                'min': await metrics_collector.get_min(MetricType.CPU_USAGE),
            },
            'memory': {
                'average': await metrics_collector.get_average(MetricType.MEMORY_USAGE),
                'max': await metrics_collector.get_max(MetricType.MEMORY_USAGE),
                'min': await metrics_collector.get_min(MetricType.MEMORY_USAGE),
            },
            'gpu': {
                'average': await metrics_collector.get_average(MetricType.GPU_USAGE),
                'max': await metrics_collector.get_max(MetricType.GPU_USAGE),
                'min': await metrics_collector.get_min(MetricType.GPU_USAGE),
            },
            'network': {
                'average_latency': await metrics_collector.get_average(MetricType.NETWORK_LATENCY),
                'max_latency': await metrics_collector.get_max(MetricType.NETWORK_LATENCY),
            },
            'tasks': {
                'average_time': await metrics_collector.get_average(MetricType.TASK_COMPLETION_TIME),
                'error_rate': await metrics_collector.get_average(MetricType.ERROR_RATE),
            }
        }
        
        # تحديد الاختناقات
        self.bottlenecks = []
        
        if analysis['cpu']['average'] > 80:
            self.bottlenecks.append("CPU مثقل جداً")
        
        if analysis['memory']['average'] > 75:
            self.bottlenecks.append("الذاكرة مثقلة جداً")
        
        if analysis['network']['average_latency'] > 100:
            self.bottlenecks.append("تأخير الشبكة مرتفع")
        
        if analysis['tasks']['error_rate'] > 0.05:
            self.bottlenecks.append("معدل الأخطاء مرتفع")
        
        return analysis
    
    async def get_recommendations(self) -> List[str]:
        """الحصول على التوصيات"""
        
        recommendations = []
        
        for bottleneck in self.bottlenecks:
            if "CPU" in bottleneck:
                recommendations.append("قلل عدد المهام المتزامنة")
                recommendations.append("استخدم GPUs للمعالجة الثقيلة")
            
            elif "الذاكرة" in bottleneck:
                recommendations.append("قلل حجم البيانات المخزنة")
                recommendations.append("استخدم التخزين المؤقت بكفاءة")
            
            elif "الشبكة" in bottleneck:
                recommendations.append("استخدم ضغط البيانات")
                recommendations.append("قلل عدد طلبات الشبكة")
            
            elif "الأخطاء" in bottleneck:
                recommendations.append("تحقق من سجلات الأخطاء")
                recommendations.append("أعد محاولة المهام الفاشلة")
        
        return recommendations


class DashboardGenerator:
    """مولد لوحة التحكم"""
    
    def __init__(self):
        self.dashboard_data = {}
    
    async def generate_dashboard(self, 
                                 metrics_collector: MetricsCollector,
                                 alert_manager: AlertManager,
                                 performance_analyzer: PerformanceAnalyzer) -> Dict:
        """توليد لوحة التحكم"""
        
        logger.info("🎨 توليد لوحة التحكم")
        
        # تحليل الأداء
        performance = await performance_analyzer.analyze_performance(metrics_collector)
        
        # التنبيهات النشطة
        active_alerts = await alert_manager.get_active_alerts()
        
        # التوصيات
        recommendations = await performance_analyzer.get_recommendations()
        
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'performance': performance,
            'alerts': {
                'total': len(alert_manager.alerts),
                'active': len(active_alerts),
                'critical': len([a for a in active_alerts if a.level == AlertLevel.CRITICAL]),
                'warnings': len([a for a in active_alerts if a.level == AlertLevel.WARNING]),
                'recent': [
                    {
                        'id': a.alert_id,
                        'level': a.level.value,
                        'message': a.message,
                        'timestamp': datetime.fromtimestamp(a.timestamp).isoformat()
                    }
                    for a in active_alerts[-10:]
                ]
            },
            'recommendations': recommendations,
            'bottlenecks': performance_analyzer.bottlenecks
        }
        
        self.dashboard_data = dashboard
        
        return dashboard


class RealtimeMonitoringSystem:
    """نظام المراقبة الفورية الرئيسي"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.performance_analyzer = PerformanceAnalyzer()
        self.dashboard_generator = DashboardGenerator()
        
        self.is_monitoring = False
        self.monitoring_interval = 1.0  # ثانية
    
    async def start_monitoring(self):
        """بدء المراقبة"""
        
        self.is_monitoring = True
        logger.info("🟢 بدء المراقبة الفورية")
        
        while self.is_monitoring:
            try:
                # جمع المقاييس
                await self._collect_metrics()
                
                # توليد لوحة التحكم
                dashboard = await self.dashboard_generator.generate_dashboard(
                    self.metrics_collector,
                    self.alert_manager,
                    self.performance_analyzer
                )
                
                await asyncio.sleep(self.monitoring_interval)
            
            except Exception as e:
                logger.error(f"❌ خطأ في المراقبة: {e}")
                await asyncio.sleep(1)
    
    async def stop_monitoring(self):
        """إيقاف المراقبة"""
        
        self.is_monitoring = False
        logger.info("🔴 إيقاف المراقبة الفورية")
    
    async def _collect_metrics(self):
        """جمع المقاييس"""
        
        current_time = datetime.now().timestamp()
        
        # محاكاة جمع المقاييس
        metrics = [
            Metric(MetricType.CPU_USAGE, np.random.uniform(20, 80), current_time, "system", "%"),
            Metric(MetricType.MEMORY_USAGE, np.random.uniform(30, 70), current_time, "system", "%"),
            Metric(MetricType.GPU_USAGE, np.random.uniform(10, 90), current_time, "gpu_0", "%"),
            Metric(MetricType.NETWORK_LATENCY, np.random.uniform(10, 100), current_time, "network", "ms"),
            Metric(MetricType.TASK_COMPLETION_TIME, np.random.uniform(100, 1000), current_time, "tasks", "ms"),
            Metric(MetricType.ERROR_RATE, np.random.uniform(0.01, 0.05), current_time, "tasks", "%"),
            Metric(MetricType.THROUGHPUT, np.random.uniform(100, 500), current_time, "system", "tasks/s"),
            Metric(MetricType.RESPONSE_TIME, np.random.uniform(50, 500), current_time, "api", "ms"),
        ]
        
        for metric in metrics:
            await self.metrics_collector.collect_metric(metric)
            
            # فحص شروط التنبيه
            alert = await self.alert_manager.check_alert_conditions(metric)
            if alert:
                await self.alert_manager.add_alert(alert)
    
    async def get_dashboard(self) -> Dict:
        """الحصول على لوحة التحكم"""
        
        return self.dashboard_generator.dashboard_data
    
    async def submit_task(self, task: Dict) -> Dict:
        """تقديم مهمة"""
        
        if task.get('type') == 'start_monitoring':
            asyncio.create_task(self.start_monitoring())
            return {'status': 'monitoring_started'}
        
        elif task.get('type') == 'stop_monitoring':
            await self.stop_monitoring()
            return {'status': 'monitoring_stopped'}
        
        elif task.get('type') == 'get_dashboard':
            dashboard = await self.get_dashboard()
            return {
                'status': 'success',
                'dashboard': dashboard
            }
        
        elif task.get('type') == 'get_alerts':
            alerts = await self.alert_manager.get_active_alerts()
            return {
                'status': 'success',
                'alerts': [
                    {
                        'id': a.alert_id,
                        'level': a.level.value,
                        'message': a.message
                    }
                    for a in alerts
                ]
            }
        
        elif task.get('type') == 'get_recommendations':
            recommendations = await self.performance_analyzer.get_recommendations()
            return {
                'status': 'success',
                'recommendations': recommendations
            }
        
        return {'status': 'error', 'message': 'نوع مهمة غير معروف'}


# مثال على الاستخدام
async def main():
    system = RealtimeMonitoringSystem()
    
    # بدء المراقبة
    monitoring_task = asyncio.create_task(system.start_monitoring())
    
    # انتظر قليلاً
    await asyncio.sleep(5)
    
    # الحصول على لوحة التحكم
    dashboard = await system.get_dashboard()
    print(f"لوحة التحكم:\n{json.dumps(dashboard, indent=2, ensure_ascii=False)}")
    
    # إيقاف المراقبة
    await system.stop_monitoring()
    await monitoring_task


if __name__ == "__main__":
    asyncio.run(main())
