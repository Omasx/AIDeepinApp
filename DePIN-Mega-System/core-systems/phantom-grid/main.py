#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    ☠️  PHANTOM GRID - MAIN ENTRY  ☠️                          ║
║                                                                                ║
║           "الشبكة الشبحية - Zero-Cost Decentralized Cloud"                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

Usage:
    python main.py                          # Run normally
    python main.py --android                # Android/Termux mode
    python main.py --daemon                 # Background mode
    python main.py --status                 # Check status
    python main.py --stealth                # Stealth mode
"""

import argparse
import asyncio
import os
import sys
import signal

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.phantom_core import PhantomCore, get_phantom


def print_banner():
    """Print Phantom Grid banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗            ║
║   ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║            ║
║   ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║            ║
║   ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║            ║
║   ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║            ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝            ║
║                                                                                ║
║                    Zero-Cost Decentralized Cloud Platform                      ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_phantom(config_path: str = None, stealth: bool = False):
    """Run Phantom Grid"""
    print_banner()
    
    phantom = get_phantom(config_path)
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print(f"\n📴 Signal {signum} received. Shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await phantom.start()
    except KeyboardInterrupt:
        print("\n👋 Phantom Grid shutdown")


async def check_status():
    """Check Phantom Grid status"""
    try:
        phantom = get_phantom()
        status = phantom.get_status()
        
        print("📊 Phantom Grid Status")
        print("=" * 50)
        print(f"Instance ID: {status['instance_id']}")
        print(f"State: {status['state']}")
        print(f"Uptime: {status['uptime']:.1f}s")
        print(f"Nodes: {status['nodes']['active']}/{status['nodes']['total']}")
        print(f"Tasks: {status['tasks']['pending']} pending")
        print(f"Battery: {status['battery']['level']}%")
        print(f"Throttle: {status['battery']['throttle']}")
        
    except Exception as e:
        print(f"❌ Status check failed: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Phantom Grid - Zero-Cost Decentralized Cloud',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to config file'
    )
    
    parser.add_argument(
        '--android', '-a',
        action='store_true',
        help='Android/Termux mode'
    )
    
    parser.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='Run as daemon'
    )
    
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Check status'
    )
    
    parser.add_argument(
        '--stealth',
        action='store_true',
        help='Stealth mode'
    )
    
    args = parser.parse_args()
    
    if args.status:
        asyncio.run(check_status())
    else:
        asyncio.run(run_phantom(args.config, args.stealth))


if __name__ == "__main__":
    main()
