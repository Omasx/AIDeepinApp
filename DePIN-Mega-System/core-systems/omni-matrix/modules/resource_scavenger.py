#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RESOURCE SCAVENGER MODULE                                 ║
║                                                                              ║
║  Zero-Cost Resource Extraction from DePIN Networks                          ║
║  - Akash Network (Free Tier)                                                ║
║  - Render Network (Community Nodes)                                         ║
║  - Golem Network (Testnet)                                                  ║
║  - iExec (Worker Pools)                                                     ║
║  - Flux Network (Parallel Assets)                                           ║
║  - Filecoin (Calibration Testnet)                                           ║
║  - Storj (Free Tier)                                                        ║
║  - IPFS (Public Gateways)                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

logger = logging.getLogger('ResourceScavenger')

@dataclass
class FreeTierAccount:
    """Represents a free tier account on a network"""
    network: str
    account_id: str
    credentials: Dict[str, str]
    quota_limit: int
    quota_used: int
    expires_at: datetime
    is_active: bool = True

class ResourceScavenger:
    """
    Scavenges free computational resources from multiple DePIN networks.
    Implements intelligent rotation and quota management.
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.config = orchestrator.config
        
        # Free tier accounts pool
        self.accounts: Dict[str, List[FreeTierAccount]] = {}
        
        # Network endpoints
        self.endpoints = {
            'akash': {
                'api': 'https://api.akashnet.io',
                'provider': 'https://provider.akashnet.io',
                'free_tier_endpoints': [
                    'https://akash-provider-1.omni-matrix.cloud',
                    'https://akash-provider-2.omni-matrix.cloud',
                ]
            },
            'render': {
                'api': 'https://api.rendernetwork.com',
                'free_tier_endpoints': [
                    'https://render-community-1.omni-matrix.cloud',
                    'https://render-community-2.omni-matrix.cloud',
                ]
            },
            'golem': {
                'api': 'https://api.golem.network',
                'testnet': 'https://testnet.golem.network',
                'free_tier_endpoints': [
                    'https://golem-testnet-1.omni-matrix.cloud',
                ]
            },
            'iexec': {
                'api': 'https://api.iex.ec',
                'free_tier_endpoints': [
                    'https://iexec-worker-1.omni-matrix.cloud',
                ]
            },
            'flux': {
                'api': 'https://api.runonflux.io',
                'free_tier_endpoints': [
                    'https://flux-node-1.omni-matrix.cloud',
                    'https://flux-node-2.omni-matrix.cloud',
                ]
            },
            'filecoin': {
                'api': 'https://api.node.glif.io',
                'calibration': 'https://api.calibration.node.glif.io',
                'free_tier_endpoints': [
                    'https://filecoin-calibration-1.omni-matrix.cloud',
                ]
            },
            'storj': {
                'api': 'https://api.storj.io',
                'free_tier_endpoints': [
                    'https://storj-free-1.omni-matrix.cloud',
                ]
            },
            'ipfs': {
                'gateways': [
                    'https://ipfs.io',
                    'https://gateway.ipfs.io',
                    'https://cloudflare-ipfs.com',
                    'https://gateway.pinata.cloud',
                    'https://ipfs.infura.io',
                    'https://dweb.link',
                    'https://ipfs.fleek.co',
                ]
            }
        }
        
        # Session for HTTP requests
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rotation counters
        self.rotation_counters = {}
        
        logger.info("🔧 Resource Scavenger initialized")
    
    async def initialize(self):
        """Initialize the scavenger"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Omni-Matrix/1.0'}
        )
        
        # Initialize free tier accounts
        await self._initialize_free_tier_accounts()
        
        logger.info("✅ Resource Scavenger ready")
    
    async def _initialize_free_tier_accounts(self):
        """Initialize free tier accounts for all networks"""
        networks = self.config['networks']
        
        for network_name, config in networks.items():
            if config['enabled'] and config['free_tier']:
                self.accounts[network_name] = []
                
                # Create multiple accounts for rotation
                for i in range(3):  # 3 accounts per network
                    account = FreeTierAccount(
                        network=network_name,
                        account_id=f"{network_name}-free-{i}",
                        credentials=self._generate_credentials(network_name, i),
                        quota_limit=self._get_quota_limit(network_name),
                        quota_used=0,
                        expires_at=datetime.now() + timedelta(days=30)
                    )
                    self.accounts[network_name].append(account)
                    
                logger.info(f"✅ Initialized {len(self.accounts[network_name])} accounts for {network_name}")
    
    def _generate_credentials(self, network: str, index: int) -> Dict[str, str]:
        """Generate credentials for free tier access"""
        # In production, these would be actual API keys/tokens
        return {
            'api_key': f"omni-matrix-{network}-{index}-{random.randint(1000, 9999)}",
            'secret': f"secret-{network}-{random.randint(10000, 99999)}",
            'endpoint': self._get_endpoint(network, index)
        }
    
    def _get_endpoint(self, network: str, index: int) -> str:
        """Get endpoint for a network"""
        endpoints = self.endpoints.get(network, {})
        
        if 'free_tier_endpoints' in endpoints:
            return endpoints['free_tier_endpoints'][index % len(endpoints['free_tier_endpoints'])]
        elif 'gateways' in endpoints:
            return endpoints['gateways'][index % len(endpoints['gateways'])]
        else:
            return endpoints.get('api', '')
    
    def _get_quota_limit(self, network: str) -> int:
        """Get quota limit for a network"""
        quotas = {
            'akash': 1000,      # 1000 deployments
            'render': 500,      # 500 render hours
            'golem': 10000,     # 10000 GLM tokens
            'iexec': 1000,      # 1000 RLC tokens
            'flux': 100,        # 100 app deployments
            'filecoin': 100,    # 100 GB storage
            'storj': 150,       # 150 GB storage
            'ipfs': 1000000,    # Unlimited (public gateways)
        }
        return quotas.get(network, 100)
    
    async def scan_network(self, network_name: str) -> List[Dict[str, Any]]:
        """Scan a network for available resources"""
        try:
            if network_name == 'akash':
                return await self._scan_akash()
            elif network_name == 'render':
                return await self._scan_render()
            elif network_name == 'golem':
                return await self._scan_golem()
            elif network_name == 'iexec':
                return await self._scan_iexec()
            elif network_name == 'flux':
                return await self._scan_flux()
            elif network_name == 'filecoin':
                return await self._scan_filecoin()
            elif network_name == 'storj':
                return await self._scan_storj()
            elif network_name == 'ipfs':
                return await self._scan_ipfs()
            else:
                logger.warning(f"⚠️ Unknown network: {network_name}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error scanning {network_name}: {e}")
            return []
    
    async def _scan_akash(self) -> List[Dict[str, Any]]:
        """Scan Akash Network for free providers"""
        resources = []
        
        try:
            # Query Akash providers
            endpoint = self.endpoints['akash']['api']
            
            async with self.session.get(f"{endpoint}/providers") as resp:
                if resp.status == 200:
                    providers = await resp.json()
                    
                    for provider in providers.get('providers', []):
                        # Check if provider offers free tier
                        if self._is_free_tier_provider('akash', provider):
                            resources.append({
                                'type': 'compute',
                                'provider': provider['owner'],
                                'endpoint': provider['host_uri'],
                                'resources': {
                                    'cpu': provider.get('resources', {}).get('cpu', 0),
                                    'memory': provider.get('resources', {}).get('memory', 0),
                                    'storage': provider.get('resources', {}).get('storage', 0)
                                },
                                'cost_per_hour': 0,  # Free tier
                                'network': 'akash'
                            })
            
            logger.info(f"🔍 Found {len(resources)} Akash providers")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Akash scan error: {e}")
            return []
    
    async def _scan_render(self) -> List[Dict[str, Any]]:
        """Scan Render Network for community nodes"""
        resources = []
        
        try:
            # Query Render community nodes
            endpoint = self.endpoints['render']['api']
            
            async with self.session.get(f"{endpoint}/nodes/community") as resp:
                if resp.status == 200:
                    nodes = await resp.json()
                    
                    for node in nodes.get('nodes', []):
                        resources.append({
                            'type': 'rendering',
                            'node_id': node['id'],
                            'endpoint': node['endpoint'],
                            'gpu': node.get('gpu', 'unknown'),
                            'resources': {
                                'gpu_memory': node.get('gpu_memory', 0),
                                'compute_units': node.get('compute_units', 0)
                            },
                            'cost_per_hour': 0,
                            'network': 'render'
                        })
            
            logger.info(f"🔍 Found {len(resources)} Render nodes")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Render scan error: {e}")
            return []
    
    async def _scan_golem(self) -> List[Dict[str, Any]]:
        """Scan Golem Network for testnet providers"""
        resources = []
        
        try:
            # Query Golem testnet
            endpoint = self.endpoints['golem']['testnet']
            
            async with self.session.get(f"{endpoint}/market/demands") as resp:
                if resp.status == 200:
                    demands = await resp.json()
                    
                    for demand in demands.get('demands', []):
                        resources.append({
                            'type': 'compute',
                            'demand_id': demand['id'],
                            'provider': demand.get('issuer'),
                            'resources': demand.get('properties', {}),
                            'cost_per_hour': 0,  # Testnet is free
                            'network': 'golem'
                        })
            
            logger.info(f"🔍 Found {len(resources)} Golem providers")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Golem scan error: {e}")
            return []
    
    async def _scan_iexec(self) -> List[Dict[str, Any]]:
        """Scan iExec for worker pools"""
        resources = []
        
        try:
            endpoint = self.endpoints['iexec']['api']
            
            async with self.session.get(f"{endpoint}/pools") as resp:
                if resp.status == 200:
                    pools = await resp.json()
                    
                    for pool in pools.get('pools', []):
                        if pool.get('is_free'):
                            resources.append({
                                'type': 'compute',
                                'pool_address': pool['address'],
                                'worker_stake': pool.get('worker_stake', 0),
                                'resources': {
                                    'cpu': pool.get('cpu', 0),
                                    'memory': pool.get('memory', 0)
                                },
                                'cost_per_task': 0,
                                'network': 'iexec'
                            })
            
            logger.info(f"🔍 Found {len(resources)} iExec pools")
            return resources
            
        except Exception as e:
            logger.error(f"❌ iExec scan error: {e}")
            return []
    
    async def _scan_flux(self) -> List[Dict[str, Any]]:
        """Scan Flux Network for parallel asset nodes"""
        resources = []
        
        try:
            endpoint = self.endpoints['flux']['api']
            
            async with self.session.get(f"{endpoint}/daemon/viewdeterministiczelnodelist") as resp:
                if resp.status == 200:
                    nodes = await resp.json()
                    
                    for node in nodes:
                        if node.get('tier') == 'CUMULUS':  # Entry tier
                            resources.append({
                                'type': 'compute',
                                'node_txhash': node['txhash'],
                                'ip': node['ip'],
                                'resources': {
                                    'vcores': 2,
                                    'ram': 4,
                                    'ssd': 50
                                },
                                'cost_per_hour': 0,
                                'network': 'flux'
                            })
            
            logger.info(f"🔍 Found {len(resources)} Flux nodes")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Flux scan error: {e}")
            return []
    
    async def _scan_filecoin(self) -> List[Dict[str, Any]]:
        """Scan Filecoin calibration testnet for storage providers"""
        resources = []
        
        try:
            endpoint = self.endpoints['filecoin']['calibration']
            
            async with self.session.post(
                f"{endpoint}/rpc/v0",
                json={"jsonrpc": "2.0", "method": "Filecoin.StateListMiners", "params": [None], "id": 1}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    miners = result.get('result', [])
                    
                    for miner in miners[:10]:  # Limit to first 10
                        resources.append({
                            'type': 'storage',
                            'miner_id': miner,
                            'endpoint': endpoint,
                            'resources': {
                                'storage_gb': 100  # Testnet allocation
                            },
                            'cost_per_gb': 0,
                            'network': 'filecoin'
                        })
            
            logger.info(f"🔍 Found {len(resources)} Filecoin miners")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Filecoin scan error: {e}")
            return []
    
    async def _scan_storj(self) -> List[Dict[str, Any]]:
        """Scan Storj for free tier storage"""
        resources = []
        
        try:
            endpoint = self.endpoints['storj']['api']
            
            async with self.session.get(f"{endpoint}/satellites") as resp:
                if resp.status == 200:
                    satellites = await resp.json()
                    
                    for sat in satellites.get('satellites', []):
                        resources.append({
                            'type': 'storage',
                            'satellite_id': sat['id'],
                            'endpoint': sat['address'],
                            'resources': {
                                'storage_gb': 150,  # Free tier
                                'bandwidth_gb': 150
                            },
                            'cost_per_gb': 0,
                            'network': 'storj'
                        })
            
            logger.info(f"🔍 Found {len(resources)} Storj satellites")
            return resources
            
        except Exception as e:
            logger.error(f"❌ Storj scan error: {e}")
            return []
    
    async def _scan_ipfs(self) -> List[Dict[str, Any]]:
        """Scan IPFS public gateways"""
        resources = []
        
        gateways = self.endpoints['ipfs']['gateways']
        
        for gateway in gateways:
            try:
                # Test gateway availability
                async with self.session.head(f"{gateway}/ipfs/QmYwAPJzv5CZsnAzt8auVK", timeout=5) as resp:
                    if resp.status in [200, 301, 302]:
                        resources.append({
                            'type': 'storage',
                            'gateway': gateway,
                            'latency_ms': 0,  # Would measure actual latency
                            'resources': {
                                'storage_gb': float('inf'),  # Unlimited
                                'bandwidth': 'unlimited'
                            },
                            'cost_per_gb': 0,
                            'network': 'ipfs'
                        })
            except:
                pass  # Gateway unavailable
        
        logger.info(f"🔍 Found {len(resources)} IPFS gateways")
        return resources
    
    def _is_free_tier_provider(self, network: str, provider: Dict) -> bool:
        """Check if a provider offers free tier resources"""
        # Check provider attributes for free tier indicators
        attributes = provider.get('attributes', [])
        
        for attr in attributes:
            key = attr.get('key', '').lower()
            value = attr.get('value', '').lower()
            
            if 'free' in key or 'free' in value:
                return True
            if 'community' in key or 'community' in value:
                return True
            if 'test' in key or 'test' in value:
                return True
        
        return False
    
    async def get_account(self, network: str) -> Optional[FreeTierAccount]:
        """Get an available free tier account for a network"""
        if network not in self.accounts:
            return None
        
        # Find account with available quota
        for account in self.accounts[network]:
            if account.is_active and account.quota_used < account.quota_limit:
                if datetime.now() < account.expires_at:
                    return account
        
        # All accounts exhausted - rotate to next set
        logger.warning(f"⚠️ All accounts exhausted for {network}, rotating...")
        await self._rotate_accounts(network)
        
        return None
    
    async def _rotate_accounts(self, network: str):
        """Rotate to new set of accounts"""
        # Reset quotas for demo purposes
        # In production, would create new accounts
        for account in self.accounts.get(network, []):
            account.quota_used = 0
            account.expires_at = datetime.now() + timedelta(days=30)
        
        logger.info(f"🔄 Rotated accounts for {network}")
    
    async def consume_quota(self, network: str, account_id: str, amount: int = 1):
        """Consume quota from an account"""
        for account in self.accounts.get(network, []):
            if account.account_id == account_id:
                account.quota_used += amount
                logger.debug(f"📊 Consumed {amount} quota from {account_id} ({account.quota_used}/{account.quota_limit})")
                break
    
    async def close(self):
        """Close the scavenger"""
        if self.session:
            await self.session.close()
            logger.info("🔒 Resource Scavenger closed")
