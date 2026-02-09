#!/usr/bin/env python3
"""
Network utilities for Omni-Matrix
"""

import socket
import asyncio
import aiohttp
from typing import Optional, Tuple


async def get_public_ip() -> Optional[str]:
    """Get public IP address"""
    services = [
        'https://api.ipify.org',
        'https://ifconfig.me/ip',
        'https://icanhazip.com'
    ]
    
    async with aiohttp.ClientSession() as session:
        for service in services:
            try:
                async with session.get(service, timeout=5) as resp:
                    if resp.status == 200:
                        return (await resp.text()).strip()
            except:
                continue
    
    return None


def get_local_ip() -> str:
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


async def test_port_open(ip: str, port: int, timeout: float = 2.0) -> bool:
    """Test if a port is open"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


async def measure_latency(host: str, port: int = 80, samples: int = 3) -> float:
    """Measure average latency to a host"""
    latencies = []
    
    for _ in range(samples):
        try:
            start = asyncio.get_event_loop().time()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=5.0
            )
            end = asyncio.get_event_loop().time()
            writer.close()
            await writer.wait_closed()
            latencies.append((end - start) * 1000)
        except:
            pass
    
    return sum(latencies) / len(latencies) if latencies else float('inf')


def get_subnet(ip: Optional[str] = None) -> str:
    """Get subnet from IP address"""
    if ip is None:
        ip = get_local_ip()
    
    parts = ip.split('.')
    return '.'.join(parts[:3])


def is_private_ip(ip: str) -> bool:
    """Check if IP is private"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        octets = [int(p) for p in parts]
    except ValueError:
        return False
    
    # 10.0.0.0/8
    if octets[0] == 10:
        return True
    
    # 172.16.0.0/12
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return True
    
    # 192.168.0.0/16
    if octets[0] == 192 and octets[1] == 168:
        return True
    
    return False
