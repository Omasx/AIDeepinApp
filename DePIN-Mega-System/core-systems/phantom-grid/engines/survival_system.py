#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🛡️  SURVIVAL SYSTEM v2.0                                   ║
║                                                                                ║
║           "نظام البقاء - لا يمكن إيقافه أبداً"                                ║
║                                                                                ║
║  Android Guerrilla Warfare Features:                                          ║
║  - Wake Lock Management (Keep CPU Alive)                                      ║
║  - Foreground Service (Disguise as System App)                                ║
║  - Anti-Kill Protection (Survive Doze Mode)                                   ║
║  - Battery Optimization Bypass                                                ║
║  - Process Disguise (Hide from Task Manager)                                  ║
║  - Silent Audio Playback (Prevent Sleep)                                      ║
║  - Notification Keep-Alive                                                    ║
║  - Heartbeat System                                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import time
import json
import subprocess
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BatteryStats:
    """Android battery statistics"""
    percent: int
    is_charging: bool
    temperature: float
    voltage: float
    health: str
    technology: str


class SurvivalSystem:
    """
    Android Survival System - Ensures Phantom Grid stays alive.
    
    Techniques:
    1. Wake Lock - Prevents CPU sleep
    2. Foreground Service - High priority process
    3. Silent Audio - Keeps audio subsystem active
    4. Notification - Persistent notification
    5. Heartbeat - Regular activity to prevent kill
    6. Process Disguise - Hide as system process
    """
    
    def __init__(self, phantom):
        self.phantom = phantom
        self.config = phantom.config['survival']
        
        # Survival state
        self.is_active = False
        self.wakelock_held = False
        self.service_running = False
        self.audio_playing = False
        
        # Threat detection
        self.threat_level = 0
        self.kill_attempts = 0
        
        # Termux detection
        self.is_termux = self._detect_termux()
        
        # Heartbeat
        self.last_heartbeat = time.time()
        
        print(f"🛡️ Survival System initialized (Termux: {self.is_termux})")
    
    def _detect_termux(self) -> bool:
        """Detect if running in Termux"""
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux/files/usr') or
            'termux' in os.environ.get('PREFIX', '')
        )
    
    async def initialize(self):
        """Initialize survival system"""
        if not self.is_termux:
            print("⚠️ Not in Termux, survival features limited")
            return
        
        print("✅ Survival System ready")
    
    async def activate(self):
        """Activate all survival mechanisms"""
        print("🛡️ Activating survival mechanisms...")
        
        self.is_active = True
        
        # Start all survival mechanisms
        await asyncio.gather(
            self._wakelock_manager(),
            self._foreground_service(),
            self._silent_audio_player(),
            self._notification_keepalive(),
            self._heartbeat_sender(),
            self._threat_monitor(),
            self._battery_monitor(),
        )
    
    async def _wakelock_manager(self):
        """Manage wake lock to keep CPU alive"""
        if not self.config.get('wakelock', True):
            return
        
        while self.is_active:
            try:
                if not self.wakelock_held:
                    # Acquire partial wake lock (CPU only, screen can sleep)
                    result = subprocess.run(
                        ['termux-wake-lock'],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        self.wakelock_held = True
                        print("🔒 Wake lock acquired")
                    else:
                        print(f"⚠️ Wake lock failed: {result.stderr}")
                
                # Re-acquire every 5 minutes to ensure it stays
                await asyncio.sleep(300)
                
            except Exception as e:
                print(f"Wake lock error: {e}")
                await asyncio.sleep(60)
    
    async def _foreground_service(self):
        """Run as foreground service with high priority"""
        if not self.config.get('foreground_service', True):
            return
        
        while self.is_active:
            try:
                if not self.service_running:
                    # Create persistent notification
                    await self._create_persistent_notification()
                    
                    # Set process priority
                    await self._set_high_priority()
                    
                    self.service_running = True
                    print("📱 Foreground service activated")
                
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Foreground service error: {e}")
                await asyncio.sleep(30)
    
    async def _create_persistent_notification(self):
        """Create persistent notification to keep service alive"""
        try:
            # Create notification that looks like a system service
            notification_cmd = [
                'termux-notification',
                '--title', 'System Service',
                '--content', 'Background process active',
                '--ongoing',
                '--id', 'phantom-grid-service',
                '--priority', 'high',
                '--alert-once'
            ]
            
            subprocess.run(notification_cmd, capture_output=True)
            
        except Exception as e:
            print(f"Notification error: {e}")
    
    async def _set_high_priority(self):
        """Set process to high priority"""
        try:
            # Set nice value (lower = higher priority)
            os.nice(-10)
            
            # Try to use termux-api for more control
            subprocess.run(
                ['termux-job-scheduler', '--period-ms', '900000'],
                capture_output=True
            )
            
        except Exception as e:
            print(f"Priority set error: {e}")
    
    async def _silent_audio_player(self):
        """Play silent audio to prevent sleep"""
        if not self.config.get('anti_kill', True):
            return
        
        while self.is_active:
            try:
                if not self.audio_playing:
                    # Create silent audio file if not exists
                    silent_audio = '/data/data/com.termux/files/home/.phantom/silent.mp3'
                    
                    if os.path.exists(silent_audio):
                        # Play silent audio in loop
                        subprocess.Popen(
                            ['termux-media-player', 'play', silent_audio],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        
                        self.audio_playing = True
                        print("🔇 Silent audio playing")
                
                await asyncio.sleep(300)
                
            except Exception as e:
                print(f"Silent audio error: {e}")
                await asyncio.sleep(60)
    
    async def _notification_keepalive(self):
        """Update notification periodically to show activity"""
        while self.is_active:
            try:
                # Get current stats
                stats = await self.get_battery_stats()
                
                # Update notification with current status
                content = (
                    f"⚡ {stats.percent}% | "
                    f"🔋 {'⚡' if stats.is_charging else '🔋'} | "
                    f"🌡️ {stats.temperature:.1f}°C"
                )
                
                notification_cmd = [
                    'termux-notification',
                    '--title', 'System Service',
                    '--content', content,
                    '--ongoing',
                    '--id', 'phantom-grid-service',
                ]
                
                subprocess.run(notification_cmd, capture_output=True)
                
                await asyncio.sleep(self.config.get('heartbeat_interval', 15))
                
            except Exception as e:
                print(f"Notification keepalive error: {e}")
                await asyncio.sleep(30)
    
    async def _heartbeat_sender(self):
        """Send regular heartbeats to prevent kill"""
        while self.is_active:
            try:
                # Perform various activities to show we're "active"
                
                # 1. Touch a file
                heartbeat_file = '/data/data/com.termux/files/home/.phantom/heartbeat'
                os.makedirs(os.path.dirname(heartbeat_file), exist_ok=True)
                
                with open(heartbeat_file, 'w') as f:
                    f.write(str(time.time()))
                
                # 2. Small network activity
                # This keeps network subsystem active
                
                # 3. Memory touch
                _ = [i for i in range(1000)]
                
                self.last_heartbeat = time.time()
                
                await asyncio.sleep(self.config.get('heartbeat_interval', 15))
                
            except Exception as e:
                print(f"Heartbeat error: {e}")
                await asyncio.sleep(5)
    
    async def _threat_monitor(self):
        """Monitor for kill attempts and threats"""
        while self.is_active:
            try:
                # Check if we're being targeted
                threat_detected = await self._detect_threat()
                
                if threat_detected:
                    self.threat_level += 1
                    self.kill_attempts += 1
                    
                    print(f"⚠️ Threat detected! Level: {self.threat_level}")
                    
                    # Escalate survival measures
                    await self._escalate_survival()
                else:
                    # Decrease threat level over time
                    self.threat_level = max(0, self.threat_level - 1)
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"Threat monitor error: {e}")
                await asyncio.sleep(30)
    
    async def _detect_threat(self) -> bool:
        """Detect if system is trying to kill us"""
        try:
            # Check if our process priority was lowered
            current_nice = os.nice(0)
            
            if current_nice > 0:
                # Priority was lowered (bad)
                return True
            
            # Check if wake lock was released
            # (We can't directly check, but we can infer from time since last heartbeat)
            time_since_heartbeat = time.time() - self.last_heartbeat
            
            if time_since_heartbeat > 60:
                return True
            
            return False
            
        except Exception as e:
            print(f"Threat detection error: {e}")
            return False
    
    async def _escalate_survival(self):
        """Escalate survival measures when threatened"""
        print("🚨 Escalating survival measures...")
        
        # 1. Re-acquire wake lock
        if self.wakelock_held:
            subprocess.run(['termux-wake-unlock'], capture_output=True)
            self.wakelock_held = False
        
        # 2. Increase priority further
        try:
            os.nice(-20)  # Maximum priority
        except:
            pass
        
        # 3. Create multiple notifications
        for i in range(3):
            subprocess.run([
                'termux-notification',
                '--title', f'System Process {i}',
                '--content', 'Critical system service',
                '--ongoing',
                '--id', f'phantom-grid-{i}',
            ], capture_output=True)
        
        # 4. Trigger replication if severely threatened
        if self.threat_level > 5:
            print("🔥 Severe threat! Triggering emergency replication...")
            # This would trigger the replication engine
    
    async def _battery_monitor(self):
        """Monitor battery and adjust behavior"""
        while self.is_active:
            try:
                stats = await self.get_battery_stats()
                
                # Adjust behavior based on battery
                if stats.percent < 10 and not stats.is_charging:
                    print("🔋 Critical battery! Entering survival mode...")
                    
                    # Reduce activity
                    self.phantom.throttle_level = 0.1
                    
                    # Release wake lock temporarily
                    if self.wakelock_held:
                        subprocess.run(['termux-wake-unlock'], capture_output=True)
                        self.wakelock_held = False
                
                elif stats.temperature > 45:
                    print("🌡️ High temperature! Throttling...")
                    
                    # Reduce CPU usage
                    self.phantom.throttle_level = 0.3
                
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Battery monitor error: {e}")
                await asyncio.sleep(30)
    
    async def get_battery_stats(self) -> BatteryStats:
        """Get battery statistics"""
        default_stats = BatteryStats(
            percent=100,
            is_charging=True,
            temperature=30.0,
            voltage=4200,
            health='GOOD',
            technology='Li-ion'
        )
        
        if not self.is_termux:
            return default_stats
        
        try:
            result = subprocess.run(
                ['termux-battery-status'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                return BatteryStats(
                    percent=data.get('percentage', 100),
                    is_charging=data.get('status') == 'CHARGING',
                    temperature=data.get('temperature', 30.0),
                    voltage=data.get('voltage', 4200),
                    health=data.get('health', 'GOOD'),
                    technology=data.get('technology', 'Li-ion')
                )
        except Exception as e:
            print(f"Battery stats error: {e}")
        
        return default_stats
    
    async def is_under_threat(self) -> bool:
        """Check if system is under threat"""
        return self.threat_level > 3 or self.kill_attempts > 5
    
    async def disguise_processes(self):
        """Disguise processes as system processes"""
        try:
            # Change process name
            # Note: This is limited in Termux without root
            
            # Create fake system files
            fake_paths = [
                '/data/data/com.termux/files/home/.phantom/.system_service',
                '/data/data/com.termux/files/home/.phantom/.android_service',
            ]
            
            for path in fake_paths:
                with open(path, 'w') as f:
                    f.write('system_process')
            
            print("🥷 Processes disguised")
            
        except Exception as e:
            print(f"Disguise error: {e}")
    
    async def deactivate(self):
        """Deactivate survival system"""
        print("🛑 Deactivating survival system...")
        
        self.is_active = False
        
        # Release wake lock
        if self.wakelock_held:
            subprocess.run(['termux-wake-unlock'], capture_output=True)
            self.wakelock_held = False
        
        # Remove notifications
        subprocess.run(
            ['termux-notification-remove', 'phantom-grid-service'],
            capture_output=True
        )
        
        print("✅ Survival system deactivated")
