"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         THE OMNI-MATRIX                                      ║
║                                                                              ║
║           Zero-Cost Decentralized Cloud Computing Platform                   ║
║                                                                              ║
║  Features:                                                                   ║
║  - 50TB Distributed Storage (IPFS, Filecoin, Storj, BitTorrent)             ║
║  - 10,000 AI Agents (DeepSeek-R1 641B Cloud)                                ║
║  - Gaming-Grade Latency (<30ms)                                             ║
║  - Multi-Network Failover (Akash, Render, Golem, iExec, Flux)               ║
║  - Self-Healing System                                                      ║
║  - Android/Termux Support                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Version: 1.0.0
Author: Chief Quantum Systems Architect & DePIN Pioneer
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Omni-Matrix Team"

from .core.orchestrator import OmniMatrixOrchestrator, get_orchestrator

__all__ = ['OmniMatrixOrchestrator', 'get_orchestrator']
