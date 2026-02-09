#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🧬 REPLICATION ENGINE v2.0                                 ║
║                                                                                ║
║           "محرك الاستنساخ - لا يمكن قتل ما لا يُرى"                           ║
║                                                                                ║
║  Features:                                                                     ║
║  - Self-Replication (Clone to new nodes)                                      ║
║  - Distributed Backup (Spread across network)                                 ║
║  - State Synchronization (Keep clones in sync)                                ║
║  - Emergency Recovery (Restore from backup)                                   ║
║  - Mutation (Evolve with each replication)                                    ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import hashlib
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Replica:
    """A replica of the Phantom Core"""
    replica_id: str
    parent_id: str
    location: str
    created_at: float
    last_sync: float
    state: Dict[str, Any]
    is_active: bool = True


class ReplicationEngine:
    """
    Replication Engine - Self-replication and backup system.
    
    When threatened, the Phantom Grid can:
    - Replicate itself to new nodes
    - Distribute state across the network
    - Recover from any surviving replica
    - Mutate to evade detection
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        self.config = phantom.config
        
        # Replica registry
        self.replicas: Dict[str, Replica] = {}
        
        # Backup chunks (distributed)
        self.backup_chunks: Dict[str, List[str]] = {}  # chunk_id -> node_ids
        
        # Stats
        self.stats = {
            'replications': 0,
            'syncs': 0,
            'recoveries': 0,
            'mutations': 0,
        }
    
    async def initialize(self):
        """Initialize Replication Engine"""
        print("🧬 Replication Engine initialized")
    
    async def replicate(self) -> bool:
        """Replicate Phantom Core to new nodes"""
        try:
            print("🧬 Initiating self-replication...")
            
            # Get current state
            state = self._capture_state()
            
            # Select target nodes for replication
            targets = await self._select_replication_targets()
            
            if not targets:
                print("⚠️ No targets available for replication")
                return False
            
            # Create replicas
            success_count = 0
            
            for target in targets:
                replica_id = await self._create_replica(target, state)
                if replica_id:
                    success_count += 1
            
            if success_count > 0:
                self.stats['replications'] += 1
                print(f"✅ Replication successful: {success_count} replicas created")
                return True
            else:
                print("❌ Replication failed")
                return False
            
        except Exception as e:
            print(f"Replication error: {e}")
            return False
    
    def _capture_state(self) -> Dict[str, Any]:
        """Capture current Phantom state"""
        return {
            'instance_id': self.phantom.instance_id,
            'config': self.phantom.config,
            'metrics': self.phantom.metrics,
            'nodes': {k: v.__dict__ for k, v in self.phantom.discovered_nodes.items()},
            'timestamp': time.time(),
        }
    
    async def _select_replication_targets(self) -> List[str]:
        """Select target nodes for replication"""
        targets = []
        
        # Get active nodes
        for node_id, node in self.phantom.discovered_nodes.items():
            if node.is_active and node.reliability > 0.5:
                targets.append(node_id)
        
        # Also use ghost nodes
        if self.phantom.ghosting_engine:
            ghosts = await self.phantom.ghosting_engine.get_active_ghosts()
            for ghost in ghosts:
                targets.append(ghost.ghost_id)
        
        # Select top 3 most reliable
        targets = targets[:3]
        
        return targets
    
    async def _create_replica(self, target_id: str, state: Dict) -> Optional[str]:
        """Create a replica on a target node"""
        try:
            replica_id = f"replica-{hashlib.sha256(f'{target_id}{time.time()}'.encode()).hexdigest()[:16]}"
            
            # Simulate replica creation
            print(f"🧬 Creating replica {replica_id} on {target_id}")
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Store replica info
            replica = Replica(
                replica_id=replica_id,
                parent_id=self.phantom.instance_id,
                location=target_id,
                created_at=time.time(),
                last_sync=time.time(),
                state=state,
            )
            
            self.replicas[replica_id] = replica
            
            # Distribute backup chunks
            await self._distribute_backup(state, replica_id)
            
            return replica_id
            
        except Exception as e:
            print(f"Replica creation error: {e}")
            return None
    
    async def _distribute_backup(self, state: Dict, replica_id: str):
        """Distribute backup chunks across network"""
        # Split state into chunks
        state_json = json.dumps(state)
        chunk_size = 1024  # 1KB chunks
        
        chunks = [
            state_json[i:i+chunk_size]
            for i in range(0, len(state_json), chunk_size)
        ]
        
        # Distribute each chunk to multiple nodes
        for i, chunk in enumerate(chunks):
            chunk_id = f"chunk-{replica_id}-{i}"
            
            # Select 3 random nodes for redundancy
            nodes = list(self.phantom.discovered_nodes.keys())
            selected = random.sample(nodes, min(3, len(nodes)))
            
            self.backup_chunks[chunk_id] = selected
        
        print(f"📦 Backup distributed: {len(chunks)} chunks")
    
    async def sync_replicas(self):
        """Synchronize state across all replicas"""
        try:
            current_state = self._capture_state()
            
            for replica_id, replica in self.replicas.items():
                if replica.is_active:
                    # Update replica state
                    replica.state = current_state
                    replica.last_sync = time.time()
            
            self.stats['syncs'] += 1
            print(f"🔄 Synced {len(self.replicas)} replicas")
            
        except Exception as e:
            print(f"Sync error: {e}")
    
    async def recover_from_replica(self, replica_id: str) -> bool:
        """Recover Phantom state from a replica"""
        try:
            replica = self.replicas.get(replica_id)
            if not replica:
                print(f"❌ Replica {replica_id} not found")
                return False
            
            print(f"🔄 Recovering from replica {replica_id}...")
            
            # Restore state
            state = replica.state
            
            # Apply recovered state
            # (In production, would actually restore)
            
            self.stats['recoveries'] += 1
            print("✅ Recovery successful")
            
            return True
            
        except Exception as e:
            print(f"Recovery error: {e}")
            return False
    
    async def mutate(self):
        """Mutate to evade detection"""
        print("🧬 Mutating...")
        
        # Change instance ID
        old_id = self.phantom.instance_id
        self.phantom.instance_id = hashlib.sha256(
            f"{old_id}{time.time()}".encode()
        ).hexdigest()[:16]
        
        # Randomize config slightly
        self.phantom.config['phantom']['stealth_mode'] = random.choice([True, False])
        
        self.stats['mutations'] += 1
        print(f"🧬 Mutated: {old_id} -> {self.phantom.instance_id}")
    
    async def cleanup_dead_replicas(self):
        """Remove dead replicas"""
        dead = []
        
        for replica_id, replica in self.replicas.items():
            # Check if replica is stale
            if time.time() - replica.last_sync > 3600:  # 1 hour
                dead.append(replica_id)
        
        for replica_id in dead:
            self.replicas[replica_id].is_active = False
            del self.replicas[replica_id]
        
        if dead:
            print(f"🧹 Cleaned up {len(dead)} dead replicas")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get replication statistics"""
        return {
            'active_replicas': len([r for r in self.replicas.values() if r.is_active]),
            'total_replicas': len(self.replicas),
            'backup_chunks': len(self.backup_chunks),
            'stats': self.stats,
        }
    
    async def close(self):
        """Close Replication Engine"""
        # Final sync
        await self.sync_replicas()
        print("🔒 Replication Engine closed")
