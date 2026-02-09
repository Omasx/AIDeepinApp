#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    ☠️ PHANTOM GRID v3.0 - MAIN ENTRY ☠️                       ║
║                                                                                ║
║  Massive Scale: Rclone + Petals + Cloudflared + Libp2p                        ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import sys
import os

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.phantom_core_v3 import main

if __name__ == "__main__":
    asyncio.run(main())
