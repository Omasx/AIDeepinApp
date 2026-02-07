#!/bin/bash

# ============================================================================
# setup.sh - سكريبت التثبيت الشامل لـ DePIN Gaming Server
# ============================================================================

set -e

echo "🔧 تجهيز بيئة DePIN Gaming Server..."
echo "=================================================="

# تحديث النظام
echo "📦 تحديث النظام..."
sudo apt update && sudo apt upgrade -y

# تثبيت الأدوات الأساسية
echo "📥 تثبيت الأدوات الأساسية..."
sudo apt install -y python3-pip python3-dev nodejs npm ffmpeg git libopencv-dev

# تحديث pip
echo "🔄 تحديث pip..."
pip3 install --upgrade pip setuptools wheel

# تثبيت المكاتب البرمجية
echo "📚 تثبيت المكاتب البرمجية..."
pip3 install -r requirements.txt

# تثبيت IPFS (اختياري)
echo "🌐 تثبيت IPFS..."
if ! command -v ipfs &> /dev/null; then
    echo "جاري تحميل IPFS..."
    wget https://dist.ipfs.io/go-ipfs/v0.19.0/go-ipfs_v0.19.0_linux-amd64.tar.gz
    tar xvfz go-ipfs_v0.19.0_linux-amd64.tar.gz
    sudo bash go-ipfs/install.sh
    rm -rf go-ipfs go-ipfs_v0.19.0_linux-amd64.tar.gz
    ipfs init
    echo "✅ IPFS تم تثبيته"
else
    echo "✅ IPFS موجود بالفعل"
fi

# إنشاء مجلدات المشروع
echo "📁 إنشاء مجلدات المشروع..."
mkdir -p logs
mkdir -p assets
mkdir -p config

# إنشاء ملف .env
echo "⚙️ إنشاء ملف الإعدادات..."
cat > .env << 'EOF'
# DePIN Gaming Server Configuration

# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
SERVER_DEBUG=true

# Solana Settings
SOLANA_NETWORK=devnet
SOLANA_RPC_URL=https://api.devnet.solana.com
SOLANA_WALLET_PATH=~/.config/solana/id.json

# IPFS Settings
IPFS_HOST=/ip4/127.0.0.1/tcp/5001
IPFS_GATEWAY=http://127.0.0.1:8080

# Game Settings
GAME_RESOLUTION=1280x720
GAME_FPS=60
GAME_BITRATE_MBPS=2.76

# Compression Settings
COMPRESSION_RATIO=0.1
QFT_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/server.log
EOF

echo "✅ اكتمل التثبيت!"
echo "=================================================="
echo ""
echo "🚀 الخطوات التالية:"
echo "1. تحديث .env بمفاتيح Solana الخاصة بك"
echo "2. تشغيل: python3 launch.py"
echo "3. افتح mobile_client.html على هاتفك"
echo ""
echo "=================================================="
