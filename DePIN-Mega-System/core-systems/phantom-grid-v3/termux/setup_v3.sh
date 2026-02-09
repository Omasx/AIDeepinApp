#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# PHANTOM GRID v3.0 - MASSIVE SCALE SETUP
# "الإعداد الضخم - دمج العمالقة"
# ═════════════════════════════════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${CYAN}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗            ║
║   ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║            ║
║   ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║            ║
║   ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║            ║
║   ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║            ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝            ║
║                                                                              ║
║                         v3.0 - MASSIVE SCALE                                 ║
║              Rclone + Petals + Cloudflared + Libp2p                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

PHANTOM_HOME="$HOME/phantom-grid-v3"
PHANTOM_BIN="$PHANTOM_HOME/bin"
mkdir -p "$PHANTOM_BIN"

echo -e "${BLUE}[1/10] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${BLUE}[2/10] Installing dependencies...${NC}"
pkg install -y \
    python python-pip git wget curl \
    termux-api termux-services \
    libffi openssl libsodium \
    rust cmake build-essential \
    clang pkg-config

# Install Python packages
echo -e "${BLUE}[3/10] Installing Python packages...${NC}"
pip install --upgrade pip
pip install -q \
    aiohttp aiofiles aiohttp-socks \
    cryptography pycryptodome pynacl \
    numpy msgpack protobuf \
    python-dotenv pyyaml click rich tqdm \
    psutil requests websockets \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    transformers accelerate bitsandbytes \
    huggingface_hub

# Download Rclone Binary
echo -e "${BLUE}[4/10] Downloading Rclone...${NC}"
RCLONE_VERSION="v1.65.0"
RCLONE_URL="https://github.com/rclone/rclone/releases/download/${RCLONE_VERSION}/rclone-${RCLONE_VERSION}-linux-arm64.zip"

cd "$PHANTOM_BIN"
if [ ! -f "rclone" ]; then
    wget -q --show-progress "$RCLONE_URL" -O rclone.zip
    unzip -q rclone.zip
    mv rclone-${RCLONE_VERSION}-linux-arm64/rclone .
    chmod +x rclone
    rm -rf rclone.zip rclone-${RCLONE_VERSION}-linux-arm64
fi
echo -e "${GREEN}✓ Rclone installed${NC}"

# Download Cloudflared Binary
echo -e "${BLUE}[5/10] Downloading Cloudflared...${NC}"
CLOUDFLARED_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"

cd "$PHANTOM_BIN"
if [ ! -f "cloudflared" ]; then
    wget -q --show-progress "$CLOUDFLARED_URL" -O cloudflared
    chmod +x cloudflared
fi
echo -e "${GREEN}✓ Cloudflared installed${NC}"

# Download IPFS Kubo
echo -e "${BLUE}[6/10] Downloading IPFS Kubo...${NC}"
IPFS_VERSION="v0.24.0"
IPFS_URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}/kubo_${IPFS_VERSION}_linux-arm64.tar.gz"

cd "$PHANTOM_BIN"
if [ ! -f "ipfs" ]; then
    wget -q --show-progress "$IPFS_URL" -O ipfs.tar.gz
    tar -xzf ipfs.tar.gz
    cp kubo/ipfs .
    chmod +x ipfs
    rm -rf kubo ipfs.tar.gz
    
    # Initialize IPFS
    ./ipfs init --profile=lowpower 2>/dev/null || true
fi
echo -e "${GREEN}✓ IPFS installed${NC}"

# Install Petals
echo -e "${BLUE}[7/10] Installing Petals...${NC}"
pip install -q git+https://github.com/bigscience-workshop/petals.git

# Download llama.cpp
echo -e "${BLUE}[8/10] Building llama.cpp...${NC}"
cd "$PHANTOM_HOME"
if [ ! -d "llama.cpp" ]; then
    git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
    cd llama.cpp
    make -j$(nproc) \
        LLAMA_NO_CUDA=1 \
        LLAMA_NO_METAL=1 \
        LLAMA_NO_VULKAN=1 \
        LLAMA_NO_BLAS=1 \
        LLAMA_NO_MPI=1
fi
echo -e "${GREEN}✓ llama.cpp built${NC}"

# Download tiny model for testing
echo -e "${BLUE}[9/10] Downloading AI models...${NC}"
mkdir -p "$PHANTOM_HOME/models"
cd "$PHANTOM_HOME/models"

if [ ! -f "tinyllama-1.1b-chat.Q4_K_M.gguf" ]; then
    wget -q --show-progress \
        "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" \
        -O tinyllama-1.1b-chat.Q4_K_M.gguf
fi
echo -e "${GREEN}✓ Models downloaded${NC}"

# Setup directories
echo -e "${BLUE}[10/10] Setting up directories...${NC}"
mkdir -p "$PHANTOM_HOME"/{storage,ai,networks,tunnels,logs,cache,config}
mkdir -p "$HOME/.phantom"/{rclone,ipfs,petals}

# Create rclone config
cat > "$HOME/.config/rclone/rclone.conf" << 'EOF'
[gdrive1]
type = drive
scope = drive
root_folder_id = 
service_account_file = 
token = 

[gdrive2]
type = drive
scope = drive

[onedrive1]
type = onedrive
token = 
drive_id = 
drive_type = personal

[dropbox1]
type = dropbox
token = 

[s3free]
type = s3
provider = AWS
env_auth = true
region = us-east-1

[phantom-union]
type = union
upstreams = gdrive1: gdrive2: onedrive1: dropbox1: s3free:
EOF

# Add to PATH
echo "export PATH=\"$PHANTOM_BIN:\$PATH\"" >> "$HOME/.bashrc"
echo "export PHANTOM_HOME=\"$PHANTOM_HOME\"" >> "$HOME/.bashrc"

# Create launcher
cat > "$PREFIX/bin/phantom" << EOF
#!/bin/bash
cd "$PHANTOM_HOME"
python3 -m core.phantom_core "\$@"
EOF
chmod +x "$PREFIX/bin/phantom"

# Create service
cat > "$HOME/.phantom/service.sh" << 'EOF'
#!/bin/bash
cd "$PHANTOM_HOME"
termux-wake-lock

# Start IPFS
$PHANTOM_BIN/ipfs daemon --enable-gc &

# Start services
python3 -m core.phantom_core --daemon
EOF
chmod +x "$HOME/.phantom/service.sh"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ SETUP COMPLETE!                                        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Binaries installed:${NC}"
echo "  - Rclone: $PHANTOM_BIN/rclone"
echo "  - Cloudflared: $PHANTOM_BIN/cloudflared"
echo "  - IPFS: $PHANTOM_BIN/ipfs"
echo "  - llama.cpp: $PHANTOM_HOME/llama.cpp"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "1. Configure Rclone: rclone config"
echo "2. Add API keys: nano $PHANTOM_HOME/config/.env"
echo "3. Start Phantom: phantom"
echo ""
echo -e "${GREEN}☠️ Phantom Grid v3.0 is ready!${NC}"
