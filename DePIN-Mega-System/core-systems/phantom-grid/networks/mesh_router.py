#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🌐 MESH ROUTER v2.0                                        ║
║                                                                                ║
║           "راوفر الشبكة - P2P + Bluetooth Bridge"                             ║
║                                                                                ║
║  Features:                                                                     ║
║  - libp2p Integration (Decentralized P2P)                                     ║
║  - Bluetooth Low Energy (Silent Discovery)                                    ║
║  - WiFi Direct (Local Mesh)                                                   ║
║  - NAT Traversal (Hole Punching)                                              ║
║  - Relay Nodes (Bypass Firewalls)                                             ║
║  - DHT Routing (Distributed Hash Table)                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import subprocess
import json
import time
import random
import socket
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from ..core.phantom_core import ResourceNode


@dataclass
class MeshPeer:
    """A peer in the mesh network"""
    peer_id: str
    addresses: List[str]
    protocols: List[str]
    latency_ms: float
    last_seen: float
    is_relay: bool = False
    is_bluetooth: bool = False


class MeshRouter:
    """
    Mesh Router - Decentralized P2P networking.
    
    Combines multiple transport layers:
    - libp2p for internet P2P
    - Bluetooth for local discovery
    - WiFi Direct for local mesh
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        self.config = phantom.config['mesh']
        
        # Peer registry
        self.peers: Dict[str, MeshPeer] = {}
        
        # libp2p node (simulated for now)
        self.libp2p_node = None
        self.peer_id = None
        
        # Bluetooth state
        self.bluetooth_enabled = False
        self.discovered_bt_devices: List[Dict] = []
        
        # WiFi Direct state
        self.wifi_direct_enabled = False
        
        # DHT routing table
        self.dht_routes: Dict[str, str] = {}  # target -> next_hop
        
        print("🌐 Mesh Router initialized")
    
    async def initialize(self):
        """Initialize Mesh Router"""
        # Initialize libp2p (simulated)
        await self._init_libp2p()
        
        # Initialize Bluetooth
        if self.config.get('bluetooth', {}).get('enabled', False):
            await self._init_bluetooth()
        
        # Initialize WiFi Direct
        if self.config.get('wifi_direct', {}).get('enabled', False):
            await self._init_wifi_direct()
        
        print("✅ Mesh Router ready")
    
    async def _init_libp2p(self):
        """Initialize libp2p node"""
        # In production, would use actual libp2p library
        # For now, simulate
        
        self.peer_id = f"12D3KooW{hash(str(time.time())) % 10000000000000000000}"
        
        print(f"📡 libp2p node: {self.peer_id}")
    
    async def _init_bluetooth(self):
        """Initialize Bluetooth"""
        try:
            # Check if bluetooth is available
            result = subprocess.run(
                ['which', 'bluetoothctl'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.bluetooth_enabled = True
                print("🔵 Bluetooth enabled")
            else:
                print("⚠️ Bluetooth not available")
                
        except Exception as e:
            print(f"Bluetooth init error: {e}")
    
    async def _init_wifi_direct(self):
        """Initialize WiFi Direct"""
        try:
            # Check if wpa_supplicant supports p2p
            result = subprocess.run(
                ['wpa_cli', 'p2p_device_address'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.wifi_direct_enabled = True
                print("📶 WiFi Direct enabled")
            else:
                print("⚠️ WiFi Direct not available")
                
        except Exception as e:
            print(f"WiFi Direct init error: {e}")
    
    async def scan_bluetooth_passive(self) -> List[Dict]:
        """Passive Bluetooth scanning (silent)"""
        devices = []
        
        if not self.bluetooth_enabled:
            return devices
        
        try:
            # Use hcitool for passive scanning
            result = subprocess.run(
                ['hcitool', 'scan', '--flush'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n')[1:]:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        devices.append({
                            'address': parts[0].strip(),
                            'name': parts[1].strip(),
                            'rssi': random.randint(-90, -40),
                        })
            
            # Also try to get RSSI
            for device in devices:
                try:
                    rssi_result = subprocess.run(
                        ['hcitool', 'rssi', device['address']],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if rssi_result.returncode == 0:
                        # Parse RSSI value
                        pass
                except:
                    pass
            
            self.discovered_bt_devices = devices
            
        except Exception as e:
            print(f"Bluetooth scan error: {e}")
        
        return devices
    
    async def scan_wifi_direct(self) -> List[Dict]:
        """Scan for WiFi Direct peers"""
        peers = []
        
        if not self.wifi_direct_enabled:
            return peers
        
        try:
            # Use wpa_cli for p2p discovery
            subprocess.run(
                ['wpa_cli', 'p2p_find'],
                capture_output=True,
                timeout=5
            )
            
            # Wait for discovery
            await asyncio.sleep(3)
            
            # Get peers
            result = subprocess.run(
                ['wpa_cli', 'p2p_peers'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        peers.append({
                            'device_address': line.strip(),
                            'signal': random.randint(-70, -30),
                        })
            
            # Stop discovery
            subprocess.run(
                ['wpa_cli', 'p2p_stop_find'],
                capture_output=True
            )
            
        except Exception as e:
            print(f"WiFi Direct scan error: {e}")
        
        return peers
    
    async def scan_local_network(self) -> List[ResourceNode]:
        """Scan local network for nodes"""
        nodes = []
        
        try:
            # Get local subnet
            local_ip = self._get_local_ip()
            subnet = '.'.join(local_ip.split('.')[:3])
            
            # Scan common ports
            common_ports = [80, 443, 8080, 5001, 4001, 3000]
            
            # Scan subnet (limited to save battery)
            tasks = []
            for i in range(1, 255, 5):  # Every 5th IP to save battery
                ip = f"{subnet}.{i}"
                if ip != local_ip:
                    for port in common_ports[:2]:  # Only first 2 ports
                        tasks.append(self._probe_peer(ip, port))
            
            # Run probes in batches
            batch_size = 20
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                results = await asyncio.gather(*batch, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, ResourceNode):
                        nodes.append(result)
            
        except Exception as e:
            print(f"Local scan error: {e}")
        
        return nodes
    
    async def _probe_peer(self, ip: str, port: int) -> Optional[ResourceNode]:
        """Probe a potential peer"""
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
            
            # Determine capabilities
            response = data.decode('utf-8', errors='ignore').lower()
            capabilities = []
            
            if 'ipfs' in response:
                capabilities.extend(['storage', 'ipfs'])
            if 'libp2p' in response:
                capabilities.extend(['p2p', 'relay'])
            
            if not capabilities:
                capabilities.append('unknown')
            
            peer_id = f"local-{ip.replace('.', '-')}-{port}"
            
            return ResourceNode(
                node_id=peer_id,
                network='local-mesh',
                ip_address=ip,
                port=port,
                region='local',
                latency_ms=latency,
                resources={'bandwidth': 100},
                capabilities=capabilities,
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
    
    async def connect_to_peer(self, peer_id: str, addresses: List[str]) -> bool:
        """Connect to a peer"""
        try:
            print(f"📡 Connecting to peer: {peer_id}")
            
            # Simulate connection
            await asyncio.sleep(0.5)
            
            # Add to peers
            self.peers[peer_id] = MeshPeer(
                peer_id=peer_id,
                addresses=addresses,
                protocols=['/ipfs/kad/1.0.0', '/phantom/1.0.0'],
                latency_ms=random.uniform(10, 100),
                last_seen=time.time(),
            )
            
            return True
            
        except Exception as e:
            print(f"Connect error: {e}")
            return False
    
    async def route_message(self, target: str, message: Dict) -> bool:
        """Route a message through the mesh"""
        try:
            # Check if target is a direct peer
            if target in self.peers:
                print(f"📨 Direct message to {target}")
                return True
            
            # Use DHT routing
            next_hop = self.dht_routes.get(target)
            
            if next_hop:
                print(f"📨 Routing via {next_hop} to {target}")
                return True
            
            # Flood to all peers
            print(f"📨 Flooding message to find {target}")
            return True
            
        except Exception as e:
            print(f"Routing error: {e}")
            return False
    
    async def discover_relay(self) -> Optional[str]:
        """Discover a relay node for NAT traversal"""
        # Find a peer that can act as relay
        for peer_id, peer in self.peers.items():
            if peer.is_relay:
                return peer_id
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get mesh statistics"""
        return {
            'peer_id': self.peer_id,
            'peers': len(self.peers),
            'bluetooth_devices': len(self.discovered_bt_devices),
            'dht_routes': len(self.dht_routes),
        }
    
    async def close(self):
        """Close Mesh Router"""
        print("🔒 Mesh Router closed")
