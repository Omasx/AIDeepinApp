"""
⚡ Auto-Failover Logic System - نظام التبديل التلقائي الذكي
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نظام متقدم للكشف عن الأخطاء والتبديل الفوري للشبكات البديلة
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import json
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """أنواع الأخطاء"""
    CONNECTION_TIMEOUT = "connection_timeout"
    NOT_FOUND_404 = "not_found_404"
    SERVER_ERROR_5XX = "server_error_5xx"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION_ERROR = "authentication_error"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    NETWORK_UNREACHABLE = "network_unreachable"
    UNKNOWN = "unknown"

class FailoverStrategy(Enum):
    """استراتيجيات التبديل"""
    IMMEDIATE = "immediate"  # تبديل فوري
    GRADUAL = "gradual"      # تبديل تدريجي
    ROUND_ROBIN = "round_robin"  # دوري
    WEIGHTED = "weighted"    # مرجح حسب الأداء

@dataclass
class ContainerState:
    """حالة الحاوية"""
    container_id: str
    current_network: str
    task_data: Dict[str, Any]
    checkpoint_data: Dict[str, Any] = field(default_factory=dict)
    execution_progress: float = 0.0  # 0-100%
    created_at: datetime = field(default_factory=datetime.now)
    last_checkpoint: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "container_id": self.container_id,
            "current_network": self.current_network,
            "task_data": self.task_data,
            "checkpoint_data": self.checkpoint_data,
            "execution_progress": self.execution_progress,
            "created_at": self.created_at.isoformat(),
            "last_checkpoint": self.last_checkpoint.isoformat() if self.last_checkpoint else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ContainerState':
        """إنشاء من قاموس"""
        return ContainerState(
            container_id=data["container_id"],
            current_network=data["current_network"],
            task_data=data["task_data"],
            checkpoint_data=data.get("checkpoint_data", {}),
            execution_progress=data.get("execution_progress", 0.0)
        )

@dataclass
class FailoverEvent:
    """حدث التبديل"""
    event_id: str
    container_id: str
    source_network: str
    target_network: str
    error_type: ErrorType
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
    recovery_time_ms: float = 0.0
    success: bool = False
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "event_id": self.event_id,
            "container_id": self.container_id,
            "source_network": self.source_network,
            "target_network": self.target_network,
            "error_type": self.error_type.value,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat(),
            "recovery_time_ms": self.recovery_time_ms,
            "success": self.success
        }

class ErrorDetector:
    """كاشف الأخطاء"""
    
    def __init__(self):
        self.error_patterns = {
            404: ErrorType.NOT_FOUND_404,
            500: ErrorType.SERVER_ERROR_5XX,
            502: ErrorType.SERVER_ERROR_5XX,
            503: ErrorType.SERVER_ERROR_5XX,
            429: ErrorType.RATE_LIMIT,
            401: ErrorType.AUTHENTICATION_ERROR,
            403: ErrorType.AUTHENTICATION_ERROR,
        }
        self.timeout_threshold = 5.0  # 5 seconds
        self.error_history: List[Tuple[str, ErrorType, datetime]] = []
    
    def detect_error(self, response_code: Optional[int], 
                    response_time: float, 
                    error_message: Optional[str] = None) -> Tuple[bool, ErrorType, str]:
        """كشف الخطأ"""
        
        # فحص timeout
        if response_time > self.timeout_threshold:
            return True, ErrorType.CONNECTION_TIMEOUT, f"Timeout after {response_time:.2f}s"
        
        # فحص رموز الخطأ
        if response_code is None:
            return True, ErrorType.NETWORK_UNREACHABLE, "Network unreachable"
        
        if response_code in self.error_patterns:
            error_type = self.error_patterns[response_code]
            return True, error_type, f"HTTP {response_code}: {error_message or ''}"
        
        # فحص رسالة الخطأ
        if error_message:
            if "exhausted" in error_message.lower():
                return True, ErrorType.RESOURCE_EXHAUSTED, error_message
            if "timeout" in error_message.lower():
                return True, ErrorType.CONNECTION_TIMEOUT, error_message
        
        return False, ErrorType.UNKNOWN, ""
    
    def record_error(self, network: str, error_type: ErrorType, timestamp: datetime = None):
        """تسجيل الخطأ"""
        if timestamp is None:
            timestamp = datetime.now()
        self.error_history.append((network, error_type, timestamp))
    
    def get_error_rate(self, network: str, minutes: int = 5) -> float:
        """الحصول على معدل الخطأ"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_errors = [
            e for e in self.error_history
            if e[0] == network and e[2] > cutoff_time
        ]
        return len(recent_errors)

class StatePreserver:
    """حفظ حالة المعالجة"""
    
    def __init__(self):
        self.saved_states: Dict[str, ContainerState] = {}
        self.checkpoint_interval = 30  # ثانية
    
    def create_checkpoint(self, container: ContainerState) -> Dict:
        """إنشاء نقطة تفتيش"""
        checkpoint = {
            "container_id": container.container_id,
            "task_data": container.task_data,
            "progress": container.execution_progress,
            "timestamp": datetime.now().isoformat(),
            "state_hash": self._calculate_hash(container)
        }
        
        container.checkpoint_data = checkpoint
        container.last_checkpoint = datetime.now()
        self.saved_states[container.container_id] = container
        
        logger.info(f"💾 Checkpoint created for {container.container_id}")
        return checkpoint
    
    def restore_from_checkpoint(self, container_id: str) -> Optional[ContainerState]:
        """استعادة من نقطة تفتيش"""
        if container_id not in self.saved_states:
            logger.warning(f"⚠️ No checkpoint found for {container_id}")
            return None
        
        container = self.saved_states[container_id]
        logger.info(f"♻️ Restored {container_id} from checkpoint")
        return container
    
    def _calculate_hash(self, container: ContainerState) -> str:
        """حساب hash للحالة"""
        state_str = json.dumps(container.to_dict(), sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()

class FailoverOrchestrator:
    """منسق التبديل"""
    
    def __init__(self, available_networks: List[str]):
        self.available_networks = available_networks
        self.active_containers: Dict[str, ContainerState] = {}
        self.error_detector = ErrorDetector()
        self.state_preserver = StatePreserver()
        self.failover_events: List[FailoverEvent] = []
        self.network_priority: Dict[str, int] = {net: i for i, net in enumerate(available_networks)}
        self.failover_strategy = FailoverStrategy.IMMEDIATE
    
    async def monitor_container(self, container: ContainerState, 
                               health_check_fn) -> Optional[FailoverEvent]:
        """مراقبة الحاوية"""
        
        while container.container_id in self.active_containers:
            try:
                # فحص صحة الشبكة
                start_time = time.time()
                response_code, error_msg = await health_check_fn(container.current_network)
                response_time = time.time() - start_time
                
                # كشف الأخطاء
                has_error, error_type, error_detail = self.error_detector.detect_error(
                    response_code, response_time, error_msg
                )
                
                if has_error:
                    logger.error(f"❌ Error detected on {container.current_network}: {error_detail}")
                    self.error_detector.record_error(container.current_network, error_type)
                    
                    # تنفيذ التبديل
                    failover_event = await self.execute_failover(container, error_type, error_detail)
                    return failover_event
                
                # تحديث checkpoint دوري
                if (datetime.now() - (container.last_checkpoint or container.created_at)).seconds > self.state_preserver.checkpoint_interval:
                    self.state_preserver.create_checkpoint(container)
                
                await asyncio.sleep(5)  # فحص كل 5 ثواني
            
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                await asyncio.sleep(5)
        
        return None
    
    async def execute_failover(self, container: ContainerState, 
                              error_type: ErrorType, 
                              error_message: str) -> FailoverEvent:
        """تنفيذ التبديل"""
        
        source_network = container.current_network
        target_network = await self._select_target_network(source_network)
        
        if not target_network:
            logger.error("❌ No alternative network available!")
            return FailoverEvent(
                event_id=self._generate_event_id(),
                container_id=container.container_id,
                source_network=source_network,
                target_network="NONE",
                error_type=error_type,
                error_message=error_message,
                success=False
            )
        
        logger.info(f"🔄 Initiating failover: {source_network} → {target_network}")
        
        start_time = time.time()
        
        try:
            # حفظ الحالة
            checkpoint = self.state_preserver.create_checkpoint(container)
            
            # استعادة على الشبكة الجديدة
            restored_container = self.state_preserver.restore_from_checkpoint(container.container_id)
            
            if restored_container:
                restored_container.current_network = target_network
                self.active_containers[container.container_id] = restored_container
                
                recovery_time = (time.time() - start_time) * 1000
                
                failover_event = FailoverEvent(
                    event_id=self._generate_event_id(),
                    container_id=container.container_id,
                    source_network=source_network,
                    target_network=target_network,
                    error_type=error_type,
                    error_message=error_message,
                    recovery_time_ms=recovery_time,
                    success=True
                )
                
                self.failover_events.append(failover_event)
                
                logger.info(f"✅ Failover successful in {recovery_time:.2f}ms")
                logger.info(f"📊 Container {container.container_id} now running on {target_network}")
                logger.info(f"📈 Progress preserved: {restored_container.execution_progress}%")
                
                return failover_event
        
        except Exception as e:
            logger.error(f"❌ Failover execution failed: {e}")
        
        recovery_time = (time.time() - start_time) * 1000
        return FailoverEvent(
            event_id=self._generate_event_id(),
            container_id=container.container_id,
            source_network=source_network,
            target_network=target_network,
            error_type=error_type,
            error_message=error_message,
            recovery_time_ms=recovery_time,
            success=False
        )
    
    async def _select_target_network(self, current_network: str) -> Optional[str]:
        """اختيار الشبكة البديلة"""
        
        # استبعاد الشبكة الحالية
        candidates = [net for net in self.available_networks if net != current_network]
        
        if not candidates:
            return None
        
        if self.failover_strategy == FailoverStrategy.IMMEDIATE:
            # اختيار الأولى المتاحة
            return candidates[0]
        
        elif self.failover_strategy == FailoverStrategy.WEIGHTED:
            # اختيار حسب الأداء (أقل معدل خطأ)
            error_rates = {net: self.error_detector.get_error_rate(net) for net in candidates}
            return min(error_rates, key=error_rates.get)
        
        elif self.failover_strategy == FailoverStrategy.ROUND_ROBIN:
            # دوري
            return candidates[0]
        
        return candidates[0]
    
    def register_container(self, container_id: str, network: str, task_data: Dict):
        """تسجيل حاوية جديدة"""
        container = ContainerState(
            container_id=container_id,
            current_network=network,
            task_data=task_data
        )
        self.active_containers[container_id] = container
        logger.info(f"📦 Container {container_id} registered on {network}")
        return container
    
    def unregister_container(self, container_id: str):
        """إلغاء تسجيل الحاوية"""
        if container_id in self.active_containers:
            del self.active_containers[container_id]
            logger.info(f"🗑️ Container {container_id} unregistered")
    
    def get_statistics(self) -> Dict:
        """الحصول على الإحصائيات"""
        total_events = len(self.failover_events)
        successful_failovers = len([e for e in self.failover_events if e.success])
        failed_failovers = total_events - successful_failovers
        
        avg_recovery_time = (
            sum(e.recovery_time_ms for e in self.failover_events) / total_events
            if total_events > 0 else 0
        )
        
        error_distribution = {}
        for event in self.failover_events:
            error_type = event.error_type.value
            error_distribution[error_type] = error_distribution.get(error_type, 0) + 1
        
        return {
            "total_failover_events": total_events,
            "successful_failovers": successful_failovers,
            "failed_failovers": failed_failovers,
            "success_rate": (successful_failovers / total_events * 100) if total_events > 0 else 0,
            "avg_recovery_time_ms": avg_recovery_time,
            "active_containers": len(self.active_containers),
            "error_distribution": error_distribution
        }
    
    def _generate_event_id(self) -> str:
        """توليد معرف الحدث"""
        return f"failover-{int(time.time() * 1000)}"

# مثال على الاستخدام
async def main():
    print("⚡ Auto-Failover System - مثال على الاستخدام")
    print("=" * 80)
    
    networks = ["akash", "render", "golem", "iexec"]
    orchestrator = FailoverOrchestrator(networks)
    
    # تسجيل حاوية
    container = orchestrator.register_container(
        container_id="container-001",
        network="akash",
        task_data={"type": "compute", "cpu": 4}
    )
    
    print(f"\n📦 Container Status:")
    print(f"  ID: {container.container_id}")
    print(f"  Network: {container.current_network}")
    print(f"  Progress: {container.execution_progress}%")
    
    # محاكاة فحص صحة
    async def mock_health_check(network: str) -> Tuple[Optional[int], Optional[str]]:
        await asyncio.sleep(0.1)
        # محاكاة خطأ على akash
        if network == "akash":
            return 503, "Service Unavailable"
        return 200, None
    
    # مراقبة الحاوية
    print(f"\n⏱️ Monitoring container...")
    failover_event = await orchestrator.monitor_container(container, mock_health_check)
    
    if failover_event:
        print(f"\n🔄 Failover Event:")
        print(f"  Source: {failover_event.source_network}")
        print(f"  Target: {failover_event.target_network}")
        print(f"  Error: {failover_event.error_type.value}")
        print(f"  Recovery Time: {failover_event.recovery_time_ms:.2f}ms")
        print(f"  Success: {failover_event.success}")
    
    # الإحصائيات
    print(f"\n📊 Statistics:")
    stats = orchestrator.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
