#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    👻 GHOSTING ENGINE v2.0                                    ║
║                                                                                ║
║           "محرك الأشباح - عقد سحابية مؤقتة لا تُقهر"                          ║
║                                                                                ║
║  Features:                                                                     ║
║  - Ephemeral Node Creation (1-hour lifetime)                                  ║
║  - Multi-Cloud Deployment (AWS, GCP, Azure free tiers)                        ║
║  - Auto-Rotation (Destroy and recreate)                                       ║
║  - Fingerprint Randomization (Avoid detection)                                ║
║  - Resource Harvesting (Idle CPU cycles)                                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import time
import random
import hashlib
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..core.phantom_core import ResourceNode


@dataclass
class GhostNode:
    """An ephemeral ghost node"""
    ghost_id: str
    cloud_provider: str
    region: str
    ip_address: str
    created_at: float
    expires_at: float
    resources: Dict[str, Any]
    fingerprint: str
    is_active: bool = True


class GhostingEngine:
    """
    Ghosting Engine - Creates ephemeral cloud nodes.
    
    Like digital ghosts, these nodes:
    - Appear and disappear randomly
    - Have randomized fingerprints
    - Harvest resources while alive
    - Auto-destruct to avoid detection
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        self.config = phantom.config['ghosting']
        
        # Ghost nodes registry
        self.ghosts: Dict[str, GhostNode] = {}
        
        # Cloud provider configurations
        self.cloud_providers = {
            'aws': {
                'free_tier': True,
                'regions': ['us-east-1', 'us-west-2', 'eu-west-1'],
                'instance_types': ['t2.micro', 't3.micro'],
                'lifetime': 3600,  # 1 hour
            },
            'gcp': {
                'free_tier': True,
                'regions': ['us-central1', 'europe-west1', 'asia-east1'],
                'instance_types': ['f1-micro', 'g1-small'],
                'lifetime': 3600,
            },
            'azure': {
                'free_tier': True,
                'regions': ['eastus', 'westeurope', 'southeastasia'],
                'instance_types': ['Standard_B1s', 'Standard_B1ls'],
                'lifetime': 3600,
            },
            'oracle': {
                'free_tier': True,
                'regions': ['us-ashburn-1', 'eu-frankfurt-1'],
                'instance_types': ['VM.Standard.E2.1.Micro'],
                'lifetime': 3600,
            },
            'ibm': {
                'free_tier': True,
                'regions': ['us-south', 'eu-gb'],
                'instance_types': ['cx2-2x4'],
                'lifetime': 3600,
            },
        }
        
        # HTTP session
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Stats
        self.stats = {
            'ghosts_created': 0,
            'ghosts_destroyed': 0,
            'resources_harvested': 0,
        }
    
    async def initialize(self):
        """Initialize Ghosting Engine"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Phantom-Ghost/2.0'}
        )
        
        print("👻 Ghosting Engine initialized")
    
    async def create_ephemeral_node(self, task=None) -> Optional[ResourceNode]:
        """Create a new ephemeral ghost node"""
        try:
            # Select cloud provider
            provider = random.choice(list(self.cloud_providers.keys()))
            config = self.cloud_providers[provider]
            
            # Generate unique ghost ID
            ghost_id = f"ghost-{provider}-{int(time.time())}-{uuid.uuid4().hex[:8]}"
            
            # Generate random fingerprint
            fingerprint = self._generate_fingerprint()
            
            # Select region and instance type
            region = random.choice(config['regions'])
            instance_type = random.choice(config['instance_types'])
            
            # Simulate node creation (in production, would use actual cloud APIs)
            print(f"👻 Creating ghost node: {ghost_id}")
            
            # Simulate creation delay
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Generate fake IP
            ip_address = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            
            # Create ghost node
            lifetime = self.config.get('ephemeral_lifetime', 3600)
            
            ghost = GhostNode(
                ghost_id=ghost_id,
                cloud_provider=provider,
                region=region,
                ip_address=ip_address,
                created_at=time.time(),
                expires_at=time.time() + lifetime,
                resources={
                    'cpu_cores': random.randint(1, 4),
                    'memory_gb': random.randint(1, 8),
                    'storage_gb': random.randint(10, 100),
                    'instance_type': instance_type,
                },
                fingerprint=fingerprint,
            )
            
            self.ghosts[ghost_id] = ghost
            self.stats['ghosts_created'] += 1
            
            print(f"✅ Ghost node created: {ghost_id} ({provider}/{region})")
            
            # Convert to ResourceNode
            node = ResourceNode(
                node_id=ghost_id,
                network=f"ghost-{provider}",
                endpoint=ip_address,
                region=region,
                latency_ms=random.uniform(20, 150),
                resources=ghost.resources,
                quota_remaining=random.randint(100, 500),
                is_free_tier=True,
            )
            
            return node
            
        except Exception as e:
            print(f"Ghost creation error: {e}")
            return None
    
    def _generate_fingerprint(self) -> str:
        """Generate random browser/system fingerprint"""
        fingerprints = [
            # Linux Chrome
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Linux Firefox
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
            # macOS Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            # Windows Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        ]
        
        return random.choice(fingerprints)
    
    async def destroy_ghost(self, ghost_id: str):
        """Destroy a ghost node"""
        try:
            ghost = self.ghosts.get(ghost_id)
            if not ghost:
                return
            
            print(f"💀 Destroying ghost: {ghost_id}")
            
            # Simulate destruction
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
            ghost.is_active = False
            del self.ghosts[ghost_id]
            
            self.stats['ghosts_destroyed'] += 1
            
            print(f"✅ Ghost destroyed: {ghost_id}")
            
        except Exception as e:
            print(f"Ghost destruction error: {e}")
    
    async def cleanup_expired(self):
        """Clean up expired ghost nodes"""
        current_time = time.time()
        expired = []
        
        for ghost_id, ghost in self.ghosts.items():
            if ghost.expires_at < current_time:
                expired.append(ghost_id)
        
        for ghost_id in expired:
            await self.destroy_ghost(ghost_id)
        
        if expired:
            print(f"🧹 Cleaned up {len(expired)} expired ghosts")
    
    async def rotate_ghosts(self):
        """Rotate ghost nodes (destroy old, create new)"""
        print("🔄 Rotating ghost nodes...")
        
        # Destroy oldest ghosts
        sorted_ghosts = sorted(
            self.ghosts.values(),
            key=lambda g: g.created_at
        )
        
        to_destroy = sorted_ghosts[:len(sorted_ghosts)//2]
        
        for ghost in to_destroy:
            await self.destroy_ghost(ghost.ghost_id)
        
        # Create new ghosts
        for _ in range(len(to_destroy)):
            await self.create_ephemeral_node()
    
    async def get_active_ghosts(self) -> List[GhostNode]:
        """Get all active ghost nodes"""
        return [g for g in self.ghosts.values() if g.is_active]
    
    async def harvest_from_ghost(self, ghost_id: str) -> Dict[str, Any]:
        """Harvest resources from a ghost node"""
        ghost = self.ghosts.get(ghost_id)
        if not ghost or not ghost.is_active:
            return {}
        
        # Simulate resource harvesting
        harvested = {
            'cpu_cycles': random.randint(1000, 10000),
            'memory_mb': ghost.resources.get('memory_gb', 1) * 100,
            'storage_mb': ghost.resources.get('storage_gb', 10) * 10,
        }
        
        self.stats['resources_harvested'] += sum(harvested.values())
        
        return harvested
    
    async def execute_on_ghost(self, task, ghost_id: str) -> Dict[str, Any]:
        """Execute a task on a ghost node"""
        ghost = self.ghosts.get(ghost_id)
        if not ghost or not ghost.is_active:
            return {'error': 'Ghost not found or inactive'}
        
        # Simulate task execution
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        return {
            'status': 'success',
            'ghost_id': ghost_id,
            'task_id': task.task_id,
            'provider': ghost.cloud_provider,
            'region': ghost.region,
            'result': {'message': 'Task executed on ghost node'}
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get ghosting statistics"""
        return {
            'active_ghosts': len([g for g in self.ghosts.values() if g.is_active]),
            'total_ghosts': len(self.ghosts),
            'stats': self.stats,
        }
    
    async def close(self):
        """Close Ghosting Engine and destroy all ghosts"""
        print("👻 Destroying all ghost nodes...")
        
        for ghost_id in list(self.ghosts.keys()):
            await self.destroy_ghost(ghost_id)
        
        if self.session:
            await self.session.close()
        
        print("🔒 Ghosting Engine closed")
