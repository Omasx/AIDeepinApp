#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE OMNI-MATRIX ORCHESTRATOR v1.0                         ║
║          Chief Quantum Systems Architect & DePIN Pioneer                     ║
║                                                                              ║
║  Zero-Cost Infrastructure | Decentralized Cloud | Self-Healing System       ║
╚══════════════════════════════════════════════════════════════════════════════╝

The Brain of the Omni-Matrix - Coordinates all subsystems, manages resources,
and ensures 100% uptime through intelligent failover mechanisms.
"""

import asyncio
import json
import logging
import signal
import sys
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading
from concurrent.futures import ThreadPoolExecutor
import hashlib
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/mnt/okcomputer/output/omni-matrix/logs/omni-matrix.log')
    ]
)
logger = logging.getLogger('OmniMatrix')

class SystemState(Enum):
    """System operational states"""
    INITIALIZING = "initializing"
    SCANNING = "scanning"
    CONNECTING = "connecting"
    ACTIVE = "active"
    DEGRADED = "degraded"
    FAILOVER = "failover"
    HEALING = "healing"
    SHUTDOWN = "shutdown"

class ResourceType(Enum):
    """Types of scavenged resources"""
    COMPUTE = "compute"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    AI_INFERENCE = "ai_inference"
    RENDERING = "rendering"

@dataclass
class NodeProfile:
    """Profile of a discovered node"""
    node_id: str
    ip_address: str
    port: int
    region: str
    latency_ms: float
    resources: Dict[str, Any]
    capabilities: List[str]
    reliability_score: float = 0.0
    last_seen: float = field(default_factory=time.time)
    is_active: bool = True

@dataclass
class TaskPacket:
    """Task to be distributed across the network"""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    priority: int
    target_resources: Dict[str, Any]
    created_at: float
    ttl: int = 300  # Time to live in seconds

class OmniMatrixOrchestrator:
    """
    The Omni-Matrix Orchestrator - Central command for the decentralized cloud
    
    Features:
    - Zero-cost resource scavenging
    - Multi-network failover
    - Self-healing capabilities
    - Edge computing optimization
    - AI task distribution
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.instance_id = str(uuid.uuid4())[:8]
        self.state = SystemState.INITIALIZING
        self.start_time = time.time()
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # Subsystems
        self.resource_scavenger = None
        self.network_mesh = None
        self.storage_sharder = None
        self.ai_dispatcher = None
        self.latency_optimizer = None
        self.self_healer = None
        
        # State management
        self.discovered_nodes: Dict[str, NodeProfile] = {}
        self.active_tasks: Dict[str, TaskPacket] = {}
        self.available_networks: List[str] = []
        self.resource_pools = defaultdict(list)
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=32)
        self._shutdown_event = threading.Event()
        self._lock = threading.RLock()
        
        # Metrics
        self.metrics = {
            'tasks_processed': 0,
            'nodes_discovered': 0,
            'data_transferred_tb': 0.0,
            'failover_count': 0,
            'healing_operations': 0
        }
        
        logger.info(f"🚀 Omni-Matrix Orchestrator initialized [ID: {self.instance_id}]")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            'networks': {
                'akash': {'enabled': True, 'priority': 1, 'free_tier': True},
                'render': {'enabled': True, 'priority': 2, 'free_tier': True},
                'golem': {'enabled': True, 'priority': 3, 'free_tier': True},
                'iexec': {'enabled': True, 'priority': 4, 'free_tier': True},
                'flux': {'enabled': True, 'priority': 5, 'free_tier': True},
                'filecoin': {'enabled': True, 'priority': 1, 'free_tier': True},
                'storj': {'enabled': True, 'priority': 2, 'free_tier': True},
                'ipfs': {'enabled': True, 'priority': 3, 'free_tier': True},
            },
            'ai': {
                'deepseek_r1_endpoint': 'cloud.deepseek.ai',
                'max_concurrent_agents': 10000,
                'inference_timeout': 30,
                'fallback_models': ['gpt-4', 'claude-3', 'llama-3']
            },
            'storage': {
                'total_capacity_tb': 50,
                'redundancy_factor': 3,
                'shard_size_mb': 64,
                'erasure_coding': True
            },
            'latency': {
                'target_gaming_latency_ms': 30,
                'edge_caching_enabled': True,
                'udp_protocol': True,
                'frame_buffer_size': 3
            },
            'android': {
                'heartbeat_interval': 30,
                'background_mode': True,
                ' opportunistic_scanning': True,
                'min_battery_percent': 15
            },
            'self_healing': {
                'enabled': True,
                'error_threshold': 5,
                'auto_fix': True,
                'github_search': True,
                'stackoverflow_search': True
            }
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info(f"✅ Configuration loaded from {config_path}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load config: {e}. Using defaults.")
        
        return default_config
    
    async def initialize_subsystems(self):
        """Initialize all subsystems"""
        logger.info("🔧 Initializing subsystems...")
        self.state = SystemState.INITIALIZING
        
        # Import and initialize subsystems
        from ..modules.resource_scavenger import ResourceScavenger
        from ..modules.network_mesh import NetworkMesh
        from ..modules.storage_sharder import StorageSharder
        from ..modules.ai_dispatcher import AIDispatcher
        from ..modules.latency_optimizer import LatencyOptimizer
        from ..modules.self_healer import SelfHealer
        
        self.resource_scavenger = ResourceScavenger(self)
        self.network_mesh = NetworkMesh(self)
        self.storage_sharder = StorageSharder(self)
        self.ai_dispatcher = AIDispatcher(self)
        self.latency_optimizer = LatencyOptimizer(self)
        self.self_healer = SelfHealer(self)
        
        # Initialize all subsystems concurrently
        await asyncio.gather(
            self.resource_scavenger.initialize(),
            self.network_mesh.initialize(),
            self.storage_sharder.initialize(),
            self.ai_dispatcher.initialize(),
            self.latency_optimizer.initialize(),
            self.self_healer.initialize()
        )
        
        logger.info("✅ All subsystems initialized successfully")
    
    async def start(self):
        """Start the Omni-Matrix orchestrator"""
        logger.info("🌟 Starting Omni-Matrix...")
        
        # Initialize
        await self.initialize_subsystems()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Start main loops
        self.state = SystemState.ACTIVE
        
        await asyncio.gather(
            self._resource_scanning_loop(),
            self._node_health_loop(),
            self._task_distribution_loop(),
            self._failover_monitor_loop(),
            self._metrics_collection_loop(),
            self._self_healing_loop()
        )
    
    async def _resource_scanning_loop(self):
        """Continuously scan for free resources"""
        while not self._shutdown_event.is_set():
            try:
                self.state = SystemState.SCANNING
                
                # Scan all configured networks
                networks = self.config['networks']
                for network_name, network_config in networks.items():
                    if network_config['enabled'] and network_config['free_tier']:
                        resources = await self.resource_scavenger.scan_network(network_name)
                        if resources:
                            logger.info(f"🔍 Found {len(resources)} resources on {network_name}")
                            self._add_to_resource_pool(network_name, resources)
                
                # Scan for local edge nodes
                edge_nodes = await self.network_mesh.scan_local_edge()
                for node in edge_nodes:
                    self._register_node(node)
                
                await asyncio.sleep(60)  # Scan every minute
                
            except Exception as e:
                logger.error(f"❌ Resource scanning error: {e}")
                await self.self_healer.report_error('resource_scanning', e)
                await asyncio.sleep(10)
    
    async def _node_health_loop(self):
        """Monitor node health and latency"""
        while not self._shutdown_event.is_set():
            try:
                with self._lock:
                    for node_id, node in list(self.discovered_nodes.items()):
                        # Check if node is still alive
                        if time.time() - node.last_seen > 300:  # 5 minutes timeout
                            node.is_active = False
                            logger.warning(f"⚠️ Node {node_id} marked as inactive")
                        
                        # Update latency
                        latency = await self.latency_optimizer.ping_node(node)
                        node.latency_ms = latency
                        
                        # Update reliability score
                        node.reliability_score = self._calculate_reliability(node)
                
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ Node health check error: {e}")
                await asyncio.sleep(5)
    
    async def _task_distribution_loop(self):
        """Distribute tasks across available resources"""
        while not self._shutdown_event.is_set():
            try:
                # Get pending tasks
                pending_tasks = self._get_pending_tasks()
                
                for task in pending_tasks:
                    # Find optimal node for this task
                    optimal_node = self._find_optimal_node(task)
                    
                    if optimal_node:
                        await self._execute_task(task, optimal_node)
                    else:
                        # Queue for later if no resources available
                        logger.warning(f"⏳ No resources available for task {task.task_id}")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Task distribution error: {e}")
                await self.self_healer.report_error('task_distribution', e)
                await asyncio.sleep(5)
    
    async def _failover_monitor_loop(self):
        """Monitor and execute failover when needed"""
        while not self._shutdown_event.is_set():
            try:
                # Check for network failures
                for network_name in self.available_networks:
                    is_healthy = await self.network_mesh.check_health(network_name)
                    
                    if not is_healthy:
                        logger.warning(f"🚨 Network {network_name} is down! Executing failover...")
                        self.state = SystemState.FAILOVER
                        
                        # Execute failover
                        await self._execute_failover(network_name)
                        self.metrics['failover_count'] += 1
                        
                        self.state = SystemState.ACTIVE
                
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Failover monitor error: {e}")
                await asyncio.sleep(5)
    
    async def _self_healing_loop(self):
        """Continuous self-healing and optimization"""
        while not self._shutdown_event.is_set():
            try:
                if self.config['self_healing']['enabled']:
                    # Check for errors
                    errors = await self.self_healer.get_error_queue()
                    
                    if len(errors) >= self.config['self_healing']['error_threshold']:
                        self.state = SystemState.HEALING
                        logger.info("🔧 Initiating self-healing sequence...")
                        
                        # Attempt auto-fix
                        if self.config['self_healing']['auto_fix']:
                            await self.self_healer.attempt_auto_fix(errors)
                        
                        self.metrics['healing_operations'] += 1
                        self.state = SystemState.ACTIVE
                
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ Self-healing error: {e}")
                await asyncio.sleep(10)
    
    async def _metrics_collection_loop(self):
        """Collect and log system metrics"""
        while not self._shutdown_event.is_set():
            try:
                uptime = time.time() - self.start_time
                
                metrics_report = {
                    'uptime_seconds': uptime,
                    'state': self.state.value,
                    'nodes_active': sum(1 for n in self.discovered_nodes.values() if n.is_active),
                    'nodes_total': len(self.discovered_nodes),
                    'tasks_active': len(self.active_tasks),
                    'tasks_processed': self.metrics['tasks_processed'],
                    'failover_count': self.metrics['failover_count'],
                    'healing_operations': self.metrics['healing_operations']
                }
                
                logger.info(f"📊 Metrics: {json.dumps(metrics_report, indent=2)}")
                
                await asyncio.sleep(300)  # Every 5 minutes
                
            except Exception as e:
                logger.error(f"❌ Metrics collection error: {e}")
                await asyncio.sleep(60)
    
    def _register_node(self, node: NodeProfile):
        """Register a discovered node"""
        with self._lock:
            if node.node_id not in self.discovered_nodes:
                self.discovered_nodes[node.node_id] = node
                self.metrics['nodes_discovered'] += 1
                logger.info(f"📍 Registered new node: {node.node_id} @ {node.region} ({node.latency_ms}ms)")
            else:
                # Update existing node
                self.discovered_nodes[node.node_id].last_seen = time.time()
    
    def _find_optimal_node(self, task: TaskPacket) -> Optional[NodeProfile]:
        """Find the optimal node for a task based on requirements"""
        with self._lock:
            active_nodes = [n for n in self.discovered_nodes.values() if n.is_active]
            
            if not active_nodes:
                return None
            
            # Score nodes based on task requirements
            scored_nodes = []
            for node in active_nodes:
                score = 0.0
                
                # Latency score (lower is better)
                if task.task_type == 'gaming':
                    score += max(0, 100 - node.latency_ms * 3)
                else:
                    score += max(0, 100 - node.latency_ms)
                
                # Reliability score
                score += node.reliability_score * 50
                
                # Resource matching
                for resource, requirement in task.target_resources.items():
                    if resource in node.resources:
                        if node.resources[resource] >= requirement:
                            score += 50
                        else:
                            score += (node.resources[resource] / requirement) * 25
                
                scored_nodes.append((node, score))
            
            # Return highest scored node
            if scored_nodes:
                scored_nodes.sort(key=lambda x: x[1], reverse=True)
                return scored_nodes[0][0]
            
            return None
    
    async def _execute_task(self, task: TaskPacket, node: NodeProfile):
        """Execute a task on the selected node"""
        try:
            logger.info(f"🚀 Executing task {task.task_id} on node {node.node_id}")
            
            # Route task to appropriate subsystem
            if task.task_type == 'ai_inference':
                result = await self.ai_dispatcher.dispatch(task, node)
            elif task.task_type == 'storage':
                result = await self.storage_sharder.store(task, node)
            elif task.task_type == 'gaming':
                result = await self.latency_optimizer.stream_game(task, node)
            else:
                result = await self.network_mesh.send_task(node, task)
            
            self.metrics['tasks_processed'] += 1
            del self.active_tasks[task.task_id]
            
            logger.info(f"✅ Task {task.task_id} completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Task execution failed: {e}")
            await self.self_healer.report_error('task_execution', e)
            raise
    
    async def _execute_failover(self, failed_network: str):
        """Execute failover to backup network"""
        logger.info(f"🔄 Executing failover from {failed_network}...")
        
        # Find next best network
        networks = self.config['networks']
        sorted_networks = sorted(
            networks.items(),
            key=lambda x: x[1]['priority']
        )
        
        for network_name, config in sorted_networks:
            if network_name != failed_network and config['enabled']:
                # Attempt migration
                success = await self.network_mesh.migrate_to_network(network_name)
                if success:
                    logger.info(f"✅ Failover successful to {network_name}")
                    return True
        
        logger.error("❌ All failover attempts failed!")
        return False
    
    def _calculate_reliability(self, node: NodeProfile) -> float:
        """Calculate reliability score for a node"""
        uptime = time.time() - node.last_seen
        latency_factor = max(0, 1 - (node.latency_ms / 1000))
        uptime_factor = min(1, uptime / 3600)  # Normalize to 1 hour
        return (latency_factor + uptime_factor) / 2
    
    def _add_to_resource_pool(self, network: str, resources: List[Dict]):
        """Add discovered resources to the pool"""
        self.resource_pools[network].extend(resources)
        if network not in self.available_networks:
            self.available_networks.append(network)
    
    def _get_pending_tasks(self) -> List[TaskPacket]:
        """Get all pending tasks"""
        return list(self.active_tasks.values())
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📴 Received signal {signum}. Shutting down gracefully...")
        self._shutdown_event.set()
        self.state = SystemState.SHUTDOWN
        sys.exit(0)
    
    async def submit_task(self, task_type: str, payload: Dict, priority: int = 5) -> str:
        """Submit a new task to the system"""
        task_id = hashlib.sha256(
            f"{time.time()}{json.dumps(payload)}".encode()
        ).hexdigest()[:16]
        
        task = TaskPacket(
            task_id=task_id,
            task_type=task_type,
            payload=payload,
            priority=priority,
            target_resources=payload.get('resources', {}),
            created_at=time.time()
        )
        
        self.active_tasks[task_id] = task
        logger.info(f"📋 Task submitted: {task_id} (type: {task_type})")
        return task_id
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'instance_id': self.instance_id,
            'state': self.state.value,
            'uptime': time.time() - self.start_time,
            'nodes': {
                'active': sum(1 for n in self.discovered_nodes.values() if n.is_active),
                'total': len(self.discovered_nodes)
            },
            'tasks': {
                'active': len(self.active_tasks),
                'processed': self.metrics['tasks_processed']
            },
            'networks': self.available_networks,
            'metrics': self.metrics
        }


# Singleton instance
_orchestrator: Optional[OmniMatrixOrchestrator] = None

def get_orchestrator(config_path: Optional[str] = None) -> OmniMatrixOrchestrator:
    """Get or create the singleton orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OmniMatrixOrchestrator(config_path)
    return _orchestrator


if __name__ == "__main__":
    # Create logs directory
    import os
    os.makedirs('/mnt/okcomputer/output/omni-matrix/logs', exist_ok=True)
    
    # Run the orchestrator
    orchestrator = get_orchestrator()
    
    try:
        asyncio.run(orchestrator.start())
    except KeyboardInterrupt:
        logger.info("👋 Omni-Matrix shutdown complete")
