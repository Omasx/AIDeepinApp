# ☠️ Phantom Grid v3.0 - Massive Scale

**Zero-Cost Decentralized Cloud with Rclone + Petals + Cloudflared + Libp2p**

---

## 🌟 What's New in v3.0

### Massive Scale Integration

| Component | Purpose | Capacity |
|-----------|---------|----------|
| **Rclone** | Multi-cloud storage | 50TB+ |
| **Petals** | Distributed AI | 1000+ GPUs |
| **Cloudflared** | Global tunnels | Unlimited |
| **Libp2p** | P2P mesh | 100K+ peers |

---

## 🚀 Quick Start

### Termux (Android)

```bash
# Download and run setup
curl -sSL https://raw.githubusercontent.com/phantom-grid/phantom/main/termux/setup_v3.sh | bash

# Start Phantom Grid
cd ~/phantom-grid-v3
python main.py
```

### Manual Setup

```bash
# 1. Clone repo
git clone https://github.com/phantom-grid/phantom.git
cd phantom/phantom-grid-v3

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download binaries
./termux/setup_v3.sh

# 4. Configure
cp config/example.env config/.env
nano config/.env

# 5. Run
python main.py
```

---

## 📁 Architecture

```
phantom-grid-v3/
├── ☁️ storage/
│   └── rclone_manager.py      # 50TB multi-cloud
│
├── 🌸 ai/
│   └── petals_swarm.py        # Distributed AI
│
├── 🌐 tunnels/
│   └── cloudflare_manager.py  # Global tunnels
│
├── 🔗 networks/
│   └── libp2p_router.py       # P2P mesh
│
├── ⚙️ core/
│   └── phantom_core_v3.py     # The Hive Mind
│
└── 📱 termux/
    └── setup_v3.sh            # Auto-installer
```

---

## ☁️ Rclone Manager

### Supported Cloud Providers (40+)

- Google Drive (15GB free)
- OneDrive (5GB free)
- Dropbox (2GB free)
- AWS S3 (5GB free tier)
- And 35+ more...

### Usage

```python
# Store file
await phantom.submit_task('storage', {
    'local_path': '/path/to/file',
    'remote_path': 'backups/file',
    'encrypt': True
})

# Retrieve file
await phantom.submit_task('retrieve', {
    'remote_path': 'backups/file',
    'local_path': '/path/to/save'
})
```

---

## 🌸 Petals Swarm

### Available Models

- `meta-llama/Llama-2-70b-chat-hf`
- `bigscience/bloom`
- `stabilityai/StableBeluga2`
- `deepseek-ai/deepseek-llm-67b-chat`

### Usage

```python
# AI inference
await phantom.submit_task('ai_inference', {
    'prompt': 'Write a Python function to...',
    'model': 'meta-llama/Llama-2-70b-chat-hf',
    'max_tokens': 512
})
```

---

## 🌐 Cloudflare Tunnels

### Features

- HTTPS impersonation
- NAT traversal
- Auto-reconnect
- Load balancing

### Usage

```python
# Create tunnel
await phantom.submit_task('create_tunnel', {
    'name': 'my-api',
    'port': 8080,
    'tunnel_type': 'http'
})
```

---

## 🔗 Libp2p Router

### Features

- DHT routing
- Relay discovery
- GossipSub messaging
- Bluetooth bridge

### Usage

```python
# Send P2P message
await phantom.submit_task('p2p_send', {
    'peer_id': '12D3KooW...',
    'protocol': '/phantom/1.0.0',
    'data': {'message': 'Hello'}
})
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

## ⚠️ Requirements

- Android 8+ with Termux (F-Droid)
- 2GB RAM minimum
- 5GB storage
- Internet connection

---

## 📜 License

MIT License

---

<p align="center">
  <strong>☠️ Phantom Grid v3.0 - The Hive Mind ☠️</strong>
</p>
