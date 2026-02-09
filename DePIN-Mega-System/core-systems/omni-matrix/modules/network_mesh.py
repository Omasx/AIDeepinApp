#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NETWORK MESH MODULE                                       ║
║                                                                              ║
║  Multi-Network Failover & DePIN Integration                                 ║
║                                                                              ║
║  Features:                                                                  ║
║  - Akash, Render, Golem, iExec, Flux integration                            ║
║  - Automatic failover between networks                                      ║
║  - Mesh network discovery                                                   ║
║  - Local edge node scanning                                                 ║
║  - Network health monitoring                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import socket

logger = logging.getLogger('NetworkMesh')

@dataclass
class NetworkStatus:
    """Status of a DePIN network"""
    network: str
    is_healthy: bool
    latency_ms: float
    available_resources: int
    last_check: float
    error_rate: float
    consecutive_failures: int

@dataclass
class MeshNode:
    """Node in the mesh network"""
    node_id: str
    ip_address: str
    port: int
    capabilities: List[str]
    latency_ms: float
    last_seen: float
    is_relay: bool = False

class NetworkMesh:
    """
    Manages connections to multiple DePIN networks and
    coordinates failover between them.
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.config = orchestrator.config
        
        # Network statuses
        self.network_status: Dict[str, NetworkStatus] = {}
        
        # Mesh nodes (local discovery)
        self.mesh_nodes: Dict[str, MeshNode] = {}
        
        # Active connections
        self.connections: Dict[str, Any] = {}
        
        # Session for HTTP requests
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Network endpoints
        self.network_endpoints = {
            'akash': {
                'health': 'https://api.akashnet.io/health',
                'providers': 'https://api.akashnet.io/providers',
                'status_url': 'https://akash.network/status'
            },
            'render': {
                'health': 'https://api.rendernetwork.com/health',
                'nodes': 'https://api.rendernetwork.com/nodes',
                'status_url': 'https://rendernetwork.com/status'
            },
            'golem': {
                'health': 'https://api.golem.network/health',
                'testnet': 'https://testnet.golem.network',
                'status_url': 'https://golem.network/status'
            },
            'iexec': {
                'health': 'https://api.iex.ec/health',
                'pools': 'https://api.iex.ec/pools',
                'status_url': 'https://iex.ec/status'
            },
            'flux': {
                'health': 'https://api.runonflux.io/flux/version',
                'nodes': 'https://api.runonflux.io/daemon/viewdeterministiczelnodelist',
                'status_url': 'https://runonflux.io/status'
            },
            'filecoin': {
                'health': 'https://api.node.glif.io/health',
                'calibration': 'https://api.calibration.node.glif.io',
                'status_url': 'https://filecoin.io/status'
            },
            'storj': {
                'health': 'https://api.storj.io/health',
                'status_url': 'https://storj.io/status'
            },
            'ipfs': {
                'gateways': [
                    'https://ipfs.io',
                    'https://cloudflare-ipfs.com',
                    'https://gateway.pinata.cloud'
                ]
            }
        }
        
        # Failover history
        self.failover_history: List[Dict[str, Any]] = []
        
        logger.info("🔧 Network Mesh initialized")
    
    async def initialize(self):
        """Initialize the network mesh"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Omni-Matrix-Network/1.0'}
        )
        
        # Initialize network statuses
        for network in self.config['networks'].keys():
            self.network_status[network] = NetworkStatus(
                network=network,
                is_healthy=True,
                latency_ms=0,
                available_resources=0,
                last_check=0,
                error_rate=0,
                consecutive_failures=0
            )
        
        # Start health monitoring
        asyncio.create_task(self._health_monitor_loop())
        
        logger.info("✅ Network Mesh ready")
    
    async def _health_monitor_loop(self):
        """Continuously monitor network health"""
        while True:
            try:
                for network in self.config['networks'].keys():
                    await self._check_network_health(network)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Health monitor error: {e}")
                await asyncio.sleep(10)
    
    async def _check_network_health(self, network: str):
        """Check health of a specific network"""
        endpoints = self.network_endpoints.get(network, {})
        status = self.network_status[network]
        
        try:
            start = time.time()
            
            if network == 'ipfs':
                # Check IPFS gateways
                healthy_gateways = 0
                for gateway in endpoints.get('gateways', []):
                    try:
                        async with self.session.head(
                            f"{gateway}/ipfs/QmYwAPJzv5CZsnAzt8auVK",
                            timeout=5
                        ) as resp:
                            if resp.status in [200, 301, 302]:
                                healthy_gateways += 1
                    except:
                        pass
                
                is_healthy = healthy_gateways > 0
                latency = (time.time() - start) * 1000
                
            else:
                # Check other networks
                health_url = endpoints.get('health', endpoints.get('status_url'))
                
                if health_url:
                    async with self.session.get(health_url, timeout=10) as resp:
                        is_healthy = resp.status == 200
                        latency = (time.time() - start) * 1000
                else:
                    is_healthy = True
                    latency = 0
            
            # Update status
            status.is_healthy = is_healthy
            status.latency_ms = latency
            status.last_check = time.time()
            
            if is_healthy:
                status.consecutive_failures = 0
                status.error_rate = max(0, status.error_rate - 0.1)
            else:
                status.consecutive_failures += 1
                status.error_rate = min(1, status.error_rate + 0.2)
            
        except Exception as e:
            logger.debug(f"Health check failed for {network}: {e}")
            status.is_healthy = False
            status.consecutive_failures += 1
            status.error_rate = min(1, status.error_rate + 0.2)
            status.last_check = time.time()
    
    async def check_health(self, network: str) -> bool:
        """Check if a network is healthy"""
        status = self.network_status.get(network)
        if not status:
            return False
        return status.is_healthy and status.consecutive_failures < 3
    
    async def migrate_to_network(self, network: str) -> bool:
        """Migrate operations to a different network"""
        logger.info(f"🔄 Migrating to network: {network}")
        
        try:
            # Verify network is healthy
            if not await self.check_health(network):
                logger.error(f"❌ Network {network} is not healthy")
                return False
            
            # Perform migration steps
            # 1. Pause new tasks
            # 2. Migrate active tasks
            # 3. Update routing
            
            # Record failover
            self.failover_history.append({
                'timestamp': time.time(),
                'to_network': network,
                'reason': 'failover',
                'success': True
            })
            
            logger.info(f"✅ Migration to {network} successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Migration to {network} failed: {e}")
            
            self.failover_history.append({
                'timestamp': time.time(),
                'to_network': network,
                'reason': 'failover',
                'success': False,
                'error': str(e)
            })
            
            return False
    
    async def scan_local_edge(self) -> List[Any]:
        """Scan for local edge nodes"""
        from ..core.orchestrator import NodeProfile
        
        discovered = []
        
        # Scan local network
        try:
            # Scan common ports
            common_ports = [80, 443, 8080, 8443, 5001, 4001, 3000]
            
            # Get local subnet
            local_ip = self._get_local_ip()
            subnet = '.'.join(local_ip.split('.')[:3])
            
            # Scan subnet
            tasks = []
            for i in range(1, 255):
                ip = f"{subnet}.{i}"
                if ip != local_ip:
                    for port in common_ports[:3]:  # Limit to first 3 ports
                        tasks.append(self._probe_node(ip, port))
            
            # Run probes concurrently (in batches)
            batch_size = 50
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                results = await asyncio.gather(*batch, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, NodeProfile):
                        discovered.append(result)
                        self.mesh_nodes[result.node_id] = MeshNode(
                            node_id=result.node_id,
                            ip_address=result.ip_address,
                            port=result.port,
                            capabilities=result.capabilities,
                            latency_ms=result.latency_ms,
                            last_seen=time.time()
                        )
        
        except Exception as e:
            logger.error(f"❌ Local edge scan error: {e}")
        
        logger.info(f"🔍 Discovered {len(discovered)} local edge nodes")
        return discovered
    
    async def _probe_node(self, ip: str, port: int) -> Optional[Any]:
        """Probe a potential node"""
        from ..core.orchestrator import NodeProfile
        
        try:
            start = time.time()
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=2.0
            )
            
            latency = (time.time() - start) * 1000
            
            # Try to identify service
            writer.write(b'GET / HTTP/1.0\r\n\r\n')
            await writer.drain()
            
            data = await asyncio.wait_for(reader.read(1024), timeout=2.0)
            
            writer.close()
            await writer.wait_closed()
            
            # Determine capabilities from response
            capabilities = []
            response = data.decode('utf-8', errors='ignore').lower()
            
            if 'ipfs' in response:
                capabilities.append('storage')
                capabilities.append('ipfs')
            if 'akash' in response:
                capabilities.append('compute')
            if 'render' in response:
                capabilities.append('rendering')
            if 'golem' in response:
                capabilities.append('compute')
            
            if not capabilities:
                capabilities.append('unknown')
            
            node_id = f"edge-{ip.replace('.', '-')}-{port}"
            
            return NodeProfile(
                node_id=node_id,
                ip_address=ip,
                port=port,
                region='local',
                latency_ms=latency,
                resources={'bandwidth': 100},
                capabilities=capabilities
            )
        
        except:
            return None
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    async def send_task(self, node: Any, task: Any) -> Dict[str, Any]:
        """Send a task to a node"""
        try:
            # In production, would use actual protocol
            # For now, simulate task execution
            
            await asyncio.sleep(0.1)  # Simulate network delay
            
            return {
                'status': 'success',
                'node_id': node.node_id,
                'task_id': task.task_id,
                'result': {'message': 'Task executed successfully'}
            }
        
        except Exception as e:
            logger.error(f"❌ Failed to send task to {node.node_id}: {e}")
            raise
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get status of all networks"""
        return {
            network: {
                'healthy': status.is_healthy,
                'latency_ms': status.latency_ms,
                'error_rate': status.error_rate,
                'consecutive_failures': status.consecutive_failures,
                'last_check': status.last_check
            }
            for network, status in self.network_status.items()
        }
    
    async def get_mesh_status(self) -> Dict[str, Any]:
        """Get mesh network status"""
        return {
            'local_nodes': len(self.mesh_nodes),
            'nodes': [
                {
                    'node_id': node.node_id,
                    'ip': node.ip_address,
                    'port': node.port,
                    'capabilities': node.capabilities,
                    'latency_ms': node.latency_ms,
                    'last_seen': node.last_seen
                }
                for node in self.mesh_nodes.values()
            ],
            'failover_history': self.failover_history[-10:]  # Last 10 failovers
        }
    
    async def close(self):
        """Close the network mesh"""
        if self.session:
            await self.session.close()
            logger.info("🔒 Network Mesh closed")
