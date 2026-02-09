#!/bin/bash
# Phantom Grid - Termux Setup Script
set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    PHANTOM GRID SETUP                                        ║"
echo "║              Zero-Cost Decentralized Cloud Platform                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Termux
if [ -z "$TERMUX_VERSION" ] && [ ! -d "/data/data/com.termux/files" ]; then
    echo "❌ This script must run in Termux!"
    exit 1
fi

echo "📱 Termux detected"
echo ""

# Update packages
echo "🔄 Updating packages..."
pkg update -y && pkg upgrade -y

# Install packages
echo "📦 Installing packages..."
pkg install -y python python-pip git wget curl nano termux-api \
    libffi openssl libsodium cmake build-essential

# Setup directories
mkdir -p $HOME/.phantom/{models,cache,logs,backup}
mkdir -p $HOME/phantom-grid

# Install Python packages
echo "🐍 Installing Python packages..."
pip install --upgrade pip
pip install aiohttp aiofiles cryptography numpy msgpack python-dotenv \
    pyyaml rich tqdm psutil requests websockets

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to .env"
echo "2. Run: python -m core.phantom_core"
echo ""
