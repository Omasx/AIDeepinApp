#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🌐 CLOUDFLARE TUNNEL MANAGER v3.0                          ║
║                                                                                ║
║           "مدير الأنفاق - التحايل على جدران الحماية"                          ║
║                                                                                ║
║  Features:                                                                     ║
║  - cloudflared Integration (Official binary)                                  ║
║  - HTTPS Impersonation (Looks like normal traffic)                            ║
║  - Multiple Tunnels (Load balancing)                                          ║
║  - Auto-Reconnect (Persistent connections)                                    ║
║  - Domain Cloaking (Hide behind legit domains)                                ║
║  - UDP over TCP (Tunnel any protocol)                                         ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import subprocess
import json
import os
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Tunnel:
    """A Cloudflare tunnel"""
    tunnel_id: str
    name: str
    hostname: str
    url: str
    status: str
    connections: int
    created_at: float
    is_active: bool = True


class CloudflareManager:
    """
    Cloudflare Tunnel Manager - The Impersonator.
    
    Uses cloudflared to create secure tunnels that:
    - Bypass NAT and firewalls
    - Look like normal HTTPS traffic
    - Auto-reconnect on failure
    - Load balance across multiple tunnels
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        
        # Binary path
        self.cloudflared_bin = os.path.expanduser(
            "~/phantom-grid-v3/bin/cloudflared"
        )
        
        # Configuration
        self.config_dir = os.path.expanduser("~/.cloudflared")
        self.tunnels: Dict[str, Tunnel] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        
        # Default services to tunnel
        self.services = {
            'phantom-api': {'port': 8080, 'type': 'http'},
            'phantom-p2p': {'port': 4001, 'type': 'tcp'},
            'phantom-ipfs': {'port': 5001, 'type': 'http'},
        }
        
        # Stats
        self.stats = {
            'tunnels_created': 0,
            'bytes_transferred': 0,
            'reconnections': 0,
        }
        
        print("🌐 Cloudflare Manager initialized")
    
    async def initialize(self):
        """Initialize Cloudflare Manager"""
        # Ensure binary exists
        if not os.path.exists(self.cloudflared_bin):
            print(f"⚠️ cloudflared not found at {self.cloudflared_bin}")
            return
        
        # Create config directory
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Check authentication
        await self._check_auth()
        
        print("✅ Cloudflare Manager ready")
    
    async def _check_auth(self):
        """Check if authenticated with Cloudflare"""
        try:
            result = subprocess.run(
                [self.cloudflared_bin, 'tunnel', 'list'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Authenticated with Cloudflare")
            else:
                print("⚠️ Not authenticated. Run: cloudflared login")
        
        except Exception as e:
            print(f"Auth check error: {e}")
    
    async def create_tunnel(self, name: str, port: int, 
                           tunnel_type: str = 'http') -> Optional[Tunnel]:
        """Create a new tunnel"""
        try:
            print(f"🌐 Creating tunnel: {name} -> localhost:{port}")
            
            # Generate unique tunnel ID
            tunnel_id = f"phantom-{name}-{int(time.time())}"
            
            # Create tunnel config
            config = {
                'tunnel': tunnel_id,
                'credentials-file': f'{self.config_dir}/{tunnel_id}.json',
                'ingress': [
                    {
                        'hostname': f'{name}.phantom-grid.workers.dev',
                        'service': f'{tunnel_type}://localhost:{port}',
                    },
                    {
                        'service': 'http_status:404',
                    }
                ],
            }
            
            # Save config
            config_path = f"{self.config_dir}/{tunnel_id}.yml"
            with open(config_path, 'w') as f:
                import yaml
                yaml.dump(config, f)
            
            # Start tunnel
            process = subprocess.Popen(
                [
                    self.cloudflared_bin,
                    'tunnel',
                    '--config', config_path,
                    'run',
                    tunnel_id,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            
            # Store tunnel
            tunnel = Tunnel(
                tunnel_id=tunnel_id,
                name=name,
                hostname=f'{name}.phantom-grid.workers.dev',
                url=f'https://{name}.phantom-grid.workers.dev',
                status='running',
                connections=0,
                created_at=time.time(),
            )
            
            self.tunnels[tunnel_id] = tunnel
            self.processes[tunnel_id] = process
            
            self.stats['tunnels_created'] += 1
            
            print(f"✅ Tunnel created: {tunnel.url}")
            
            return tunnel
        
        except Exception as e:
            print(f"Tunnel create error: {e}")
            return None
    
    async def start_all_tunnels(self):
        """Start tunnels for all services"""
        print("🌐 Starting all tunnels...")
        
        for service_name, config in self.services.items():
            tunnel = await self.create_tunnel(
                name=service_name,
                port=config['port'],
                tunnel_type=config['type']
            )
            
            if tunnel:
                print(f"  ✅ {service_name}: {tunnel.url}")
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(2)
        
        print(f"✅ Started {len(self.tunnels)} tunnels")
    
    async def stop_tunnel(self, tunnel_id: str):
        """Stop a tunnel"""
        try:
            tunnel = self.tunnels.get(tunnel_id)
            if not tunnel:
                return
            
            print(f"🛑 Stopping tunnel: {tunnel.name}")
            
            # Kill process
            process = self.processes.get(tunnel_id)
            if process:
                process.terminate()
                process.wait()
            
            tunnel.is_active = False
            tunnel.status = 'stopped'
        
        except Exception as e:
            print(f"Tunnel stop error: {e}")
    
    async def restart_tunnel(self, tunnel_id: str):
        """Restart a tunnel"""
        await self.stop_tunnel(tunnel_id)
        await asyncio.sleep(2)
        
        tunnel = self.tunnels.get(tunnel_id)
        if tunnel:
            await self.create_tunnel(
                name=tunnel.name,
                port=int(tunnel.url.split(':')[-1]),
            )
            
            self.stats['reconnections'] += 1
    
    async def monitor_tunnels(self):
        """Monitor and maintain tunnels"""
        while True:
            try:
                for tunnel_id, tunnel in self.tunnels.items():
                    if not tunnel.is_active:
                        continue
                    
                    # Check if process is alive
                    process = self.processes.get(tunnel_id)
                    if process and process.poll() is not None:
                        print(f"⚠️ Tunnel {tunnel.name} died, restarting...")
                        await self.restart_tunnel(tunnel_id)
                    
                    # Check tunnel health
                    healthy = await self._check_tunnel_health(tunnel)
                    if not healthy:
                        print(f"⚠️ Tunnel {tunnel.name} unhealthy, restarting...")
                        await self.restart_tunnel(tunnel_id)
                
                await asyncio.sleep(30)
            
            except Exception as e:
                print(f"Monitor error: {e}")
                await asyncio.sleep(10)
    
    async def _check_tunnel_health(self, tunnel: Tunnel) -> bool:
        """Check if tunnel is healthy"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    tunnel.url,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    # Any response means tunnel is working
                    return True
        
        except:
            return False
    
    async def get_tunnel_metrics(self, tunnel_id: str) -> Dict[str, Any]:
        """Get metrics for a tunnel"""
        tunnel = self.tunnels.get(tunnel_id)
        if not tunnel:
            return {}
        
        return {
            'tunnel_id': tunnel_id,
            'name': tunnel.name,
            'hostname': tunnel.hostname,
            'status': tunnel.status,
            'uptime': time.time() - tunnel.created_at,
            'connections': tunnel.connections,
        }
    
    async def create_quick_tunnel(self, port: int) -> Optional[str]:
        """Create a quick tunnel (no auth required)"""
        try:
            print(f"🌐 Creating quick tunnel for port {port}...")
            
            # Quick tunnels don't require auth
            result = subprocess.run(
                [
                    self.cloudflared_bin,
                    'tunnel',
                    '--url', f'http://localhost:{port}',
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse URL from output
            for line in result.stderr.split('\n'):
                if 'https://' in line and 'trycloudflare.com' in line:
                    url = line.split('https://')[1].split()[0]
                    return f"https://{url}"
            
            return None
        
        except Exception as e:
            print(f"Quick tunnel error: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tunnel statistics"""
        return {
            'tunnels': len(self.tunnels),
            'active': sum(1 for t in self.tunnels.values() if t.is_active),
            'tunnels_created': self.stats['tunnels_created'],
            'reconnections': self.stats['reconnections'],
            'urls': [t.url for t in self.tunnels.values() if t.is_active],
        }
    
    async def close(self):
        """Close all tunnels"""
        print("🌐 Closing all tunnels...")
        
        for tunnel_id in list(self.tunnels.keys()):
            await self.stop_tunnel(tunnel_id)
        
        print("🔒 Cloudflare Manager closed")
