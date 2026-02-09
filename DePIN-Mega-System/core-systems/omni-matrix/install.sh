#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# Omni-Matrix Installation Script
# Zero-Cost Decentralized Cloud Platform
# ═════════════════════════════════════════════════════════════════════════════

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    OMNI-MATRIX INSTALLER                                     ║"
echo "║              Zero-Cost Decentralized Cloud Platform                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ -n "$TERMUX_VERSION" ]]; then
    OS="termux"
fi

echo -e "${BLUE}Detected OS: $OS${NC}"
echo ""

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check pip
echo -e "${BLUE}Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${RED}✗ pip3 not found. Please install pip${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo ""
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create directories
echo ""
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p logs
mkdir -p data
mkdir -p cache
echo -e "${GREEN}✓ Directories created${NC}"

# Create .env file if not exists
echo ""
echo -e "${BLUE}Setting up environment...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created from template${NC}"
    echo -e "${YELLOW}⚠ Please edit .env with your API keys${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
fi

# Make main.py executable
echo ""
echo -e "${BLUE}Setting permissions...${NC}"
chmod +x main.py
echo -e "${GREEN}✓ Permissions set${NC}"

# Termux specific setup
if [ "$OS" == "termux" ]; then
    echo ""
    echo -e "${BLUE}Setting up Termux environment...${NC}"
    
    # Check termux-api
    if command -v termux-battery-status &> /dev/null; then
        echo -e "${GREEN}✓ termux-api installed${NC}"
    else
        echo -e "${YELLOW}⚠ termux-api not installed${NC}"
        echo -e "${BLUE}Install with: pkg install termux-api${NC}"
    fi
    
    # Create Termux shortcut
    if [ ! -f "$HOME/.shortcuts/omni-matrix" ]; then
        mkdir -p "$HOME/.shortcuts"
        cat > "$HOME/.shortcuts/omni-matrix" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/omni-matrix
source venv/bin/activate
python main.py --android
EOF
        chmod +x "$HOME/.shortcuts/omni-matrix"
        echo -e "${GREEN}✓ Termux shortcut created${NC}"
    fi
fi

# Create systemd service (Linux only)
if [ "$OS" == "linux" ] && command -v systemctl &> /dev/null; then
    echo ""
    echo -e "${BLUE}Creating systemd service...${NC}"
    
    SERVICE_FILE="/etc/systemd/system/omni-matrix.service"
    if [ ! -f "$SERVICE_FILE" ]; then
        sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Omni-Matrix Decentralized Cloud Platform
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python $(pwd)/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        echo -e "${GREEN}✓ Systemd service created${NC}"
        echo -e "${BLUE}Start with: sudo systemctl start omni-matrix${NC}"
        echo -e "${BLUE}Enable auto-start: sudo systemctl enable omni-matrix${NC}"
    else
        echo -e "${YELLOW}⚠ Systemd service already exists${NC}"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    INSTALLATION COMPLETE!                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✓ Omni-Matrix has been successfully installed!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env with your API keys (all free tiers):"
echo "   nano .env"
echo ""
echo "2. Run Omni-Matrix:"
echo "   python main.py"
echo ""
echo "3. For Android/Termux:"
echo "   python main.py --android"
echo ""
echo "4. Check status:"
echo "   python main.py --status"
echo ""
echo "Documentation: https://docs.omni-matrix.io"
echo "Support: https://discord.gg/omni-matrix"
echo ""
echo -e "${GREEN}Happy computing! 🚀${NC}"
echo ""
