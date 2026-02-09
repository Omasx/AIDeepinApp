#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ANDROID/TERMUX ADAPTER                                    ║
║                                                                              ║
║  Termux Integration for Android Devices                                     ║
║                                                                              ║
║  Features:                                                                  ║
║  - Background service management                                            ║
║  - Keep-alive heartbeat                                                     ║
║  - Opportunistic scanning                                                   ║
║  - Battery-aware operation                                                  ║
║  - Minimal resource footprint                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import json
import logging
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import time
import threading

logger = logging.getLogger('TermuxAdapter')

@dataclass
class DeviceStats:
    """Android device statistics"""
    battery_percent: int
    is_charging: bool
    available_storage_mb: int
    total_ram_mb: int
    available_ram_mb: int
    cpu_usage_percent: float
    network_type: str
    timestamp: float = field(default_factory=time.time)

class TermuxAdapter:
    """
    Adapter for running Omni-Matrix on Android via Termux.
    Manages background operation, battery optimization, and
    resource constraints.
    """
    
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.config = orchestrator.config.get('android', {}) if orchestrator else {}
        
        # Device info
        self.is_termux = self._detect_termux()
        self.device_info = self._get_device_info()
        
        # Service state
        self.is_running = False
        self.background_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # Stats
        self.current_stats: Optional[DeviceStats] = None
        self.stats_history: List[DeviceStats] = []
        
        # Wakelock
        self.wakelock_held = False
        
        logger.info(f"🔧 Termux Adapter initialized (Termux: {self.is_termux})")
    
    def _detect_termux(self) -> bool:
        """Detect if running in Termux environment"""
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux/files/usr') or
            'termux' in os.environ.get('PREFIX', '')
        )
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get Android device information"""
        info = {
            'is_termux': self.is_termux,
            'android_version': 'unknown',
            'device_model': 'unknown',
            'termux_version': os.environ.get('TERMUX_VERSION', 'unknown'),
            'architecture': os.uname().machine,
            'python_version': sys.version
        }
        
        if self.is_termux:
            try:
                # Get Android version
                result = subprocess.run(
                    ['getprop', 'ro.build.version.release'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    info['android_version'] = result.stdout.strip()
                
                # Get device model
                result = subprocess.run(
                    ['getprop', 'ro.product.model'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    info['device_model'] = result.stdout.strip()
                
            except Exception as e:
                logger.warning(f"⚠️ Could not get device info: {e}")
        
        return info
    
    async def initialize(self):
        """Initialize the Termux adapter"""
        if not self.is_termux:
            logger.warning("⚠️ Not running in Termux, some features disabled")
            return
        
        # Setup Termux environment
        await self._setup_termux_environment()
        
        # Acquire wakelock
        await self._acquire_wakelock()
        
        # Start monitoring
        asyncio.create_task(self._stats_monitoring_loop())
        
        logger.info("✅ Termux Adapter ready")
    
    async def _setup_termux_environment(self):
        """Setup Termux environment for background operation"""
        try:
            # Ensure termux-api is installed
            result = subprocess.run(
                ['which', 'termux-battery-status'],
                capture_output=True
            )
            
            if result.returncode != 0:
                logger.warning("⚠️ termux-api not installed. Battery monitoring disabled.")
                logger.info("💡 Install with: pkg install termux-api")
            
            # Create notification channel for keep-alive
            await self._create_notification_channel()
            
        except Exception as e:
            logger.error(f"❌ Termux setup error: {e}")
    
    async def _create_notification_channel(self):
        """Create persistent notification for keep-alive"""
        try:
            # Use termux-notification to create persistent notification
            notification_cmd = [
                'termux-notification',
                '--title', 'Omni-Matrix',
                '--content', 'Decentralized Cloud Node Active',
                '--ongoing',
                '--id', 'omni-matrix-service'
            ]
            
            subprocess.run(notification_cmd, capture_output=True)
            logger.info("📱 Persistent notification created")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create notification: {e}")
    
    async def _acquire_wakelock(self):
        """Acquire wake lock to keep CPU running"""
        try:
            # Use termux-wake-lock
            result = subprocess.run(
                ['termux-wake-lock'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.wakelock_held = True
                logger.info("🔒 Wake lock acquired")
            else:
                logger.warning("⚠️ Could not acquire wake lock")
                
        except Exception as e:
            logger.warning(f"⚠️ Wake lock error: {e}")
    
    async def _release_wakelock(self):
        """Release wake lock"""
        try:
            subprocess.run(['termux-wake-unlock'], capture_output=True)
            self.wakelock_held = False
            logger.info("🔓 Wake lock released")
        except Exception as e:
            logger.warning(f"⚠️ Could not release wake lock: {e}")
    
    async def _stats_monitoring_loop(self):
        """Monitor device stats continuously"""
        while not self._shutdown_event.is_set():
            try:
                stats = await self._get_device_stats()
                self.current_stats = stats
                self.stats_history.append(stats)
                
                # Keep only last 100 readings
                if len(self.stats_history) > 100:
                    self.stats_history = self.stats_history[-100:]
                
                # Check battery level
                if stats.battery_percent < self.config.get('min_battery_percent', 15):
                    logger.warning(f"🔋 Low battery: {stats.battery_percent}%. Throttling...")
                    await self._throttle_operation()
                
                # Log stats periodically
                if len(self.stats_history) % 10 == 0:
                    logger.debug(
                        f"📊 Battery: {stats.battery_percent}%, "
                        f"RAM: {stats.available_ram_mb}MB free, "
                        f"CPU: {stats.cpu_usage_percent:.1f}%"
                    )
                
                await asyncio.sleep(self.config.get('heartbeat_interval', 30))
                
            except Exception as e:
                logger.error(f"❌ Stats monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def _get_device_stats(self) -> DeviceStats:
        """Get current device statistics"""
        stats = DeviceStats(
            battery_percent=100,
            is_charging=True,
            available_storage_mb=0,
            total_ram_mb=0,
            available_ram_mb=0,
            cpu_usage_percent=0.0,
            network_type='unknown'
        )
        
        if not self.is_termux:
            return stats
        
        try:
            # Battery status
            result = subprocess.run(
                ['termux-battery-status'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                battery_data = json.loads(result.stdout)
                stats.battery_percent = battery_data.get('percentage', 100)
                stats.is_charging = battery_data.get('status') == 'CHARGING'
        except:
            pass
        
        try:
            # Storage info
            stat = os.statvfs('/data')
            stats.available_storage_mb = (stat.f_bavail * stat.f_frsize) // (1024 * 1024)
        except:
            pass
        
        try:
            # Memory info from /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                
                for line in meminfo.split('\n'):
                    if 'MemTotal:' in line:
                        stats.total_ram_mb = int(line.split()[1]) // 1024
                    elif 'MemAvailable:' in line:
                        stats.available_ram_mb = int(line.split()[1]) // 1024
        except:
            pass
        
        try:
            # CPU usage
            with open('/proc/stat', 'r') as f:
                cpu_line = f.readline()
                cpu_times = list(map(int, cpu_line.split()[1:]))
                idle_time = cpu_times[3]
                total_time = sum(cpu_times)
                stats.cpu_usage_percent = 100 * (1 - idle_time / total_time)
        except:
            pass
        
        try:
            # Network type
            result = subprocess.run(
                ['termux-network-info'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                network_data = json.loads(result.stdout)
                stats.network_type = network_data.get('type', 'unknown')
        except:
            pass
        
        return stats
    
    async def _throttle_operation(self):
        """Throttle operations to save battery"""
        logger.info("🔋 Throttling operations...")
        
        # Reduce scan frequency
        if self.orchestrator:
            # Notify orchestrator to reduce activity
            pass
    
    async def start_background_service(self):
        """Start Omni-Matrix as a background service"""
        logger.info("🚀 Starting background service...")
        
        self.is_running = True
        
        # Create startup script
        await self._create_startup_script()
        
        # Start heartbeat
        asyncio.create_task(self._heartbeat_loop())
        
        logger.info("✅ Background service started")
    
    async def _create_startup_script(self):
        """Create startup script for auto-restart"""
        try:
            script_content = """#!/data/data/com.termux/files/usr/bin/bash
# Omni-Matrix Auto-Start Script

cd /data/data/com.termux/files/home/omni-matrix
source venv/bin/activate

# Start with auto-restart
while true; do
    python -m core.orchestrator
    echo "Omni-Matrix crashed, restarting in 5 seconds..."
    sleep 5
done
"""
            script_path = '/data/data/com.termux/files/home/start-omni-matrix.sh'
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            os.chmod(script_path, 0o755)
            logger.info(f"✅ Startup script created: {script_path}")
            
        except Exception as e:
            logger.error(f"❌ Could not create startup script: {e}")
    
    async def _heartbeat_loop(self):
        """Send keep-alive heartbeat"""
        while self.is_running and not self._shutdown_event.is_set():
            try:
                # Update notification
                if self.is_termux:
                    await self._update_notification()
                
                # Log heartbeat
                logger.debug("💓 Heartbeat")
                
                await asyncio.sleep(self.config.get('heartbeat_interval', 30))
                
            except Exception as e:
                logger.error(f"❌ Heartbeat error: {e}")
                await asyncio.sleep(5)
    
    async def _update_notification(self):
        """Update persistent notification"""
        try:
            stats = self.current_stats
            if stats:
                content = (
                    f"Node Active | Battery: {stats.battery_percent}% | "
                    f"RAM: {stats.available_ram_mb}MB | "
                    f"Net: {stats.network_type}"
                )
                
                notification_cmd = [
                    'termux-notification',
                    '--title', 'Omni-Matrix',
                    '--content', content,
                    '--ongoing',
                    '--id', 'omni-matrix-service'
                ]
                
                subprocess.run(notification_cmd, capture_output=True)
                
        except Exception as e:
            logger.debug(f"Notification update failed: {e}")
    
    async def opportunistic_scan(self) -> List[Dict[str, Any]]:
        """Perform opportunistic network scan"""
        if not self.config.get('opportunistic_scanning', True):
            return []
        
        # Only scan when conditions are favorable
        if self.current_stats:
            # Don't scan on low battery
            if self.current_stats.battery_percent < 20:
                return []
            
            # Don't scan on mobile data (save bandwidth)
            if self.current_stats.network_type == 'MOBILE':
                return []
        
        logger.info("🔍 Performing opportunistic scan...")
        
        # Perform brief scan
        discovered = []
        
        # Scan local Bluetooth devices
        bt_devices = await self._scan_bluetooth()
        discovered.extend(bt_devices)
        
        # Scan local network
        if self.orchestrator:
            network_mesh = self.orchestrator.network_mesh
            if network_mesh:
                nodes = await network_mesh.scan_local_edge()
                discovered.extend([{
                    'type': 'edge_node',
                    'node_id': n.node_id,
                    'ip': n.ip_address,
                    'capabilities': n.capabilities
                } for n in nodes])
        
        return discovered
    
    async def _scan_bluetooth(self) -> List[Dict[str, Any]]:
        """Scan for Bluetooth devices"""
        devices = []
        
        if not self.is_termux:
            return devices
        
        try:
            # Use termux-bluetooth
            result = subprocess.run(
                ['termux-bluetooth-scan'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                bt_data = json.loads(result.stdout)
                for device in bt_data.get('devices', []):
                    devices.append({
                        'type': 'bluetooth',
                        'address': device.get('address'),
                        'name': device.get('name'),
                        'rssi': device.get('rssi')
                    })
        
        except Exception as e:
            logger.debug(f"Bluetooth scan failed: {e}")
        
        return devices
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get current device status"""
        return {
            'is_termux': self.is_termux,
            'device_info': self.device_info,
            'current_stats': {
                'battery_percent': self.current_stats.battery_percent if self.current_stats else None,
                'is_charging': self.current_stats.is_charging if self.current_stats else None,
                'available_ram_mb': self.current_stats.available_ram_mb if self.current_stats else None,
                'cpu_usage': self.current_stats.cpu_usage_percent if self.current_stats else None,
                'network_type': self.current_stats.network_type if self.current_stats else None
            },
            'is_running': self.is_running,
            'wakelock_held': self.wakelock_held
        }
    
    async def shutdown(self):
        """Shutdown the adapter"""
        logger.info("🛑 Shutting down Termux Adapter...")
        
        self.is_running = False
        self._shutdown_event.set()
        
        # Release wakelock
        await self._release_wakelock()
        
        # Cancel notification
        if self.is_termux:
            try:
                subprocess.run(
                    ['termux-notification-remove', 'omni-matrix-service'],
                    capture_output=True
                )
            except:
                pass
        
        logger.info("✅ Termux Adapter shutdown complete")


# Entry point for Termux
async def main():
    """Main entry point for Termux"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    OMNI-MATRIX FOR ANDROID                                   ║
║                        Termux Edition                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize adapter
    adapter = TermuxAdapter()
    await adapter.initialize()
    
    # Start background service
    await adapter.start_background_service()
    
    # Keep running
    try:
        while adapter.is_running:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await adapter.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
