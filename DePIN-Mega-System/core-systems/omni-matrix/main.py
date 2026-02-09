#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE OMNI-MATRIX                                           ║
║                                                                              ║
║              Zero-Cost Decentralized Cloud Computing Platform                ║
║                                                                              ║
║  ╔═══════════════════════════════════════════════════════════════════════╗   ║
║  ║  System Capabilities:                                                 ║   ║
║  ║  - 50TB Distributed Storage (IPFS, Filecoin, Storj, BitTorrent)       ║   ║
║  ║  - 10,000 AI Agents (DeepSeek-R1 641B via Cloud)                      ║   ║
║  ║  - Gaming-Grade Latency <30ms (Fortnite, AAA Games)                   ║   ║
║  ║  - Multi-Network Failover (Akash, Render, Golem, iExec, Flux)         ║   ║
║  ║  - Self-Healing Code with Auto-Repair                                 ║   ║
║  ║  - Android/Termux Support                                             ║   ║
║  ║  - Zero-Cost Infrastructure                                           ║   ║
║  ╚═══════════════════════════════════════════════════════════════════════╝   ║
║                                                                              ║
║  Usage: python main.py [--config PATH] [--android] [--daemon]               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import asyncio
import os
import sys
import signal
import json
from typing import Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import OmniMatrixOrchestrator, get_orchestrator


def print_banner():
    """Print system banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███╗   ███╗███╗   ██╗██╗         ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗   ║
║  ██╔═══██╗████╗ ████║████╗  ██║██║         ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝   ║
║  ██║   ██║██╔████╔██║██╔██╗ ██║██║         ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝    ║
║  ██║   ██║██║╚██╔╝██║██║╚██╗██║██║         ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗    ║
║  ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗   ║
║   ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝   ║
║                                                                              ║
║                    Zero-Cost Decentralized Cloud Platform                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_orchestrator(config_path: Optional[str] = None):
    """Run the main orchestrator"""
    print_banner()
    
    # Create logs directory
    os.makedirs('/mnt/okcomputer/output/omni-matrix/logs', exist_ok=True)
    
    # Initialize orchestrator
    orchestrator = get_orchestrator(config_path)
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print(f"\n📴 Received signal {signum}. Shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start orchestrator
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        print("\n👋 Omni-Matrix shutdown complete")


async def run_android_mode(config_path: Optional[str] = None):
    """Run in Android/Termux mode"""
    print_banner()
    print("📱 Android/Termux Mode Activated\n")
    
    from android.termux_adapter import TermuxAdapter
    
    # Initialize orchestrator
    orchestrator = get_orchestrator(config_path)
    
    # Initialize Android adapter
    adapter = TermuxAdapter(orchestrator)
    await adapter.initialize()
    
    # Start background service
    await adapter.start_background_service()
    
    # Start orchestrator
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        await adapter.shutdown()
        print("\n👋 Omni-Matrix Android mode shutdown complete")


async def run_daemon_mode(config_path: Optional[str] = None):
    """Run in daemon mode (background)"""
    print("👻 Running in daemon mode...")
    
    # Fork to background (Unix only)
    if os.name != 'nt':
        try:
            pid = os.fork()
            if pid > 0:
                print(f"📝 Daemon PID: {pid}")
                sys.exit(0)
        except OSError as e:
            print(f"❌ Fork failed: {e}")
            sys.exit(1)
    
    # Run orchestrator
    await run_orchestrator(config_path)


async def run_status_check():
    """Check system status"""
    print("📊 Omni-Matrix Status Check\n")
    
    # Try to connect to running instance
    try:
        orchestrator = get_orchestrator()
        status = orchestrator.get_status()
        
        print(json.dumps(status, indent=2))
        
    except Exception as e:
        print(f"❌ Could not connect to Omni-Matrix: {e}")
        print("💡 Is the system running?")


async def submit_task(task_type: str, payload: str, priority: int = 5):
    """Submit a task to the system"""
    print(f"📋 Submitting task: {task_type}\n")
    
    try:
        orchestrator = get_orchestrator()
        
        # Parse payload
        try:
            payload_dict = json.loads(payload)
        except json.JSONDecodeError:
            payload_dict = {'data': payload}
        
        # Submit task
        task_id = await orchestrator.submit_task(task_type, payload_dict, priority)
        
        print(f"✅ Task submitted: {task_id}")
        
    except Exception as e:
        print(f"❌ Failed to submit task: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='The Omni-Matrix - Zero-Cost Decentralized Cloud Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run in normal mode
  python main.py --android                # Run in Android/Termux mode
  python main.py --daemon                 # Run as background daemon
  python main.py --status                 # Check system status
  python main.py --task ai_inference --payload '{"prompt": "Hello"}'
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='config/default.json',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--android', '-a',
        action='store_true',
        help='Run in Android/Termux mode'
    )
    
    parser.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='Run as background daemon'
    )
    
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Check system status'
    )
    
    parser.add_argument(
        '--task', '-t',
        type=str,
        choices=['ai_inference', 'storage', 'gaming', 'compute'],
        help='Submit a task'
    )
    
    parser.add_argument(
        '--payload', '-p',
        type=str,
        default='{}',
        help='Task payload (JSON string)'
    )
    
    parser.add_argument(
        '--priority',
        type=int,
        default=5,
        choices=range(1, 11),
        help='Task priority (1-10)'
    )
    
    args = parser.parse_args()
    
    # Run appropriate mode
    if args.status:
        asyncio.run(run_status_check())
    elif args.task:
        asyncio.run(submit_task(args.task, args.payload, args.priority))
    elif args.android:
        asyncio.run(run_android_mode(args.config))
    elif args.daemon:
        asyncio.run(run_daemon_mode(args.config))
    else:
        asyncio.run(run_orchestrator(args.config))


if __name__ == "__main__":
    main()
