# ☠️ Phantom Grid

**Zero-Cost Decentralized Cloud Computing Platform**

[![Version](https://img.shields.io/badge/version-2.0.0-red.svg)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

---

## 🌟 Vision

**Phantom Grid** is the world's most aggressive zero-cost decentralized cloud platform. It scavenges free resources from multiple DePIN networks to create an unstoppable, self-healing, infinitely scalable cloud infrastructure that runs on your Android phone.

### Key Capabilities

| Feature | Specification |
|---------|--------------|
| 🧠 **AI** | llama.cpp Local + DeepSeek Cloud |
| 🌐 **Network** | libp2P + Bluetooth Bridge |
| 💾 **Storage** | 50TB+ (IPFS, Filecoin, Storj) |
| 🎮 **Gaming** | <30ms Latency (Moonlight) |
| 🧛 **Resources** | Vampire Engine (Free Tier Scavenging) |
| 🛡️ **Survival** | Anti-Kill System for Android |
| 👻 **Ghosting** | Ephemeral Cloud Nodes |
| 🧬 **Replication** | Self-Replication when Threatened |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHANTOM GRID                                      │
│                    Zero-Cost Decentralized Cloud                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   VAMPIRE    │  │   GHOSTING   │  │  SURVIVAL    │  │ REPLICATION  │   │
│  │   ENGINE     │  │   ENGINE     │  │   SYSTEM     │  │   ENGINE     │   │
│  │              │  │              │  │              │  │              │   │
│  │ 🧛 Scavenge  │  │ 👻 Ephemeral │  │ 🛡️ Anti-Kill │  │ 🧬 Self-Clone│   │
│  │ Free Tiers   │  │ Nodes        │  │ Wake Lock    │  │ Backup       │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                 │                 │            │
│  ┌──────┴─────────────────┴─────────────────┴─────────────────┴───────┐   │
│  │                      PHANTOM CORE                                   │   │
│  │         (Task Distribution, Failover, State Management)             │   │
│  └──────┬─────────────────┬─────────────────┬─────────────────┬───────┘   │
│         │                 │                 │                 │            │
│  ┌──────▼──────┐  ┌───────▼────────┐  ┌────▼──────┐  ┌───────▼───────┐   │
│  │   LLAMA     │  │     MESH       │  │  PHANTOM  │  │   MOONLIGHT   │   │
│  │   BRIDGE    │  │   ROUTER       │  │  STORAGE  │  │    ADAPTER    │   │
│  │             │  │                │  │           │  │               │   │
│  │ Local AI    │  │ libp2P + BT    │  │ 50TB      │  │ Game Stream   │   │
│  │ Cloud Offload│  │ WiFi Direct    │  │ IPFS      │  │ <30ms         │   │
│  └─────────────┘  └────────────────┘  └───────────┘  └───────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Android/Termux Installation

```bash
# 1. Install Termux from F-Droid (NOT Play Store)
# https://f-droid.org/packages/com.termux/

# 2. Run setup script in Termux
curl -sSL https://raw.githubusercontent.com/phantom-grid/phantom/main/termux/setup.sh | bash

# 3. Add your API keys (all free tiers)
nano ~/phantom-grid/.env

# 4. Start Phantom Grid
python ~/phantom-grid/main.py
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/phantom-grid/phantom.git
cd phantom

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## 📱 Android Features

### Survival System (Anti-Kill)

- 🔒 **Wake Lock** - Prevents CPU sleep
- 📱 **Foreground Service** - High priority process
- 🔇 **Silent Audio** - Keeps audio subsystem active
- 🔔 **Persistent Notification** - Shows as system service
- 💓 **Heartbeat** - Regular activity to prevent kill
- 🥷 **Process Disguise** - Hides from task manager

### Battery Optimization

- 📊 **Adaptive Throttling** - Reduces activity on low battery
- 🔋 **Smart Charging Detection** - Full speed when charging
- 🌡️ **Temperature Monitoring** - Throttles when hot
- ⚡ **Priority Tasks** - Critical tasks only on low battery

---

## 🧛 Vampire Engine

The Vampire Engine scavenges free resources from:

| Network | Type | Free Tier | Accounts |
|---------|------|-----------|----------|
| Akash | Compute | ✅ | 5 rotating |
| Render | Rendering | ✅ | 3 rotating |
| Golem | Compute | ✅ Testnet | 10 |
| iExec | Compute | ✅ | 5 rotating |
| Flux | Compute | ✅ | 5 rotating |
| Filecoin | Storage | ✅ Testnet | 10 |
| Storj | Storage | ✅ 150GB | 3 rotating |

### Account Rotation

```python
# Automatically rotates accounts before quota exhaustion
await vampire_engine.rotate_accounts()
```

---

## 👻 Ghosting Engine

Creates ephemeral cloud nodes that:
- Appear and disappear randomly
- Have randomized fingerprints
- Auto-destruct after 1 hour
- Harvest resources while alive

```python
# Create ghost node
ghost = await ghosting_engine.create_ephemeral_node()

# It will auto-destruct after lifetime expires
```

---

## 🧠 AI (Llama Bridge)

### Local Inference (llama.cpp)

```python
# Local inference (battery efficient)
result = await ai_engine.execute(task)
```

### Cloud Offloading

```python
# Automatically offloads to cloud when:
# - Context is large (>2K tokens)
# - Battery is low (<30%)
# - Local model unavailable
```

### Supported Models

- TinyLlama 1.1B (default, fast)
- Llama-2 7B (balanced)
- DeepSeek Coder 1.3B (coding)
- Mistral 7B (powerful)

---

## 🌐 Mesh Network

### Bluetooth Bridge (Passive)

```python
# Silent discovery of nearby devices
devices = await mesh_router.scan_bluetooth_passive()
```

### WiFi Direct

```python
# Local mesh without internet
peers = await mesh_router.scan_wifi_direct()
```

### libp2P Integration

```python
# Decentralized P2P networking
await mesh_router.connect_to_peer(peer_id, addresses)
```

---

## 💾 Storage (50TB)

### Backends

- **IPFS** - Content-addressed storage
- **Filecoin** - Decentralized storage market
- **Storj** - Encrypted distributed storage
- **BitTorrent** - P2P file sharing

### Usage

```python
# Store data
result = await storage.store(data=b'Hello', name='test.txt')

# Retrieve data
result = await storage.retrieve(object_id)
```

---

## 🎮 Gaming (Moonlight)

### Supported Games

- Fortnite
- Apex Legends
- Valorant
- Counter-Strike 2
- League of Legends

### Adaptive Quality

```python
# Automatically adjusts based on:
# - Network conditions
# - Battery level
# - Device temperature
```

---

## 🧬 Self-Replication

When threatened, Phantom Grid can:

1. **Replicate** to new nodes
2. **Distribute** state across network
3. **Recover** from any surviving replica
4. **Mutate** to evade detection

```python
# Trigger replication
await replication_engine.replicate()

# Mutate to evade detection
await replication_engine.mutate()
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# AI APIs
export DEEPSEEK_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"

# Performance
export PHANTOM_MAX_BATTERY_DRAIN=15
export PHANTOM_STEALTH_MODE=true
```

### Config File (config.json)

```json
{
  "phantom": {
    "stealth_mode": true,
    "max_battery_drain": 15
  },
  "ai": {
    "max_local_agents": 10,
    "offload_to_cloud": true
  },
  "survival": {
    "wakelock": true,
    "anti_kill": true
  }
}
```

---

## 📊 Monitoring

```bash
# Check status
python main.py --status

# View logs
tail -f ~/.phantom/logs/phantom.log
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

---

## 📜 License

MIT License - See LICENSE file

---

## ⚠️ Disclaimer

This software is for educational purposes only. Users are responsible for complying with:
- Terms of Service of cloud providers
- Local laws and regulations
- Battery and device safety

---

<p align="center">
  <strong>☠️ Built with 💙 by the Phantom Grid Team ☠️</strong><br>
  <em>"We are the ghosts in the machine"</em>
</p>
