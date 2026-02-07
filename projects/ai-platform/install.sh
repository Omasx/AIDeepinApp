#!/bin/bash

# ============================================================================
# AI DePIN Cloud Platform - Installation Script
# ============================================================================

set -e

echo "🚀 بدء تثبيت منصة AI DePIN Cloud..."
echo "=================================================="

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# الدوال
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# التحقق من Python
print_status "التحقق من Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 غير مثبت!"
    exit 1
fi
print_success "Python 3 موجود"

# التحقق من pip
print_status "التحقق من pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 غير مثبت!"
    exit 1
fi
print_success "pip3 موجود"

# إنشاء بيئة افتراضية
print_status "إنشاء بيئة افتراضية..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "تم إنشاء البيئة الافتراضية"
else
    print_warning "البيئة الافتراضية موجودة بالفعل"
fi

# تفعيل البيئة الافتراضية
print_status "تفعيل البيئة الافتراضية..."
source venv/bin/activate
print_success "تم تفعيل البيئة الافتراضية"

# تحديث pip
print_status "تحديث pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_success "تم تحديث pip"

# تثبيت المكاتب المطلوبة
print_status "تثبيت المكاتب المطلوبة..."
echo "هذا قد يستغرق عدة دقائق..."

pip install -r backend/requirements.txt

print_success "تم تثبيت جميع المكاتب"

# إنشاء مجلدات التخزين
print_status "إنشاء مجلدات التخزين..."
mkdir -p backend/sessions
mkdir -p backend/logs
mkdir -p backend/cache
mkdir -p frontend/assets
print_success "تم إنشاء المجلدات"

# إنشاء ملف .env
print_status "إنشاء ملف الإعدادات..."
if [ ! -f "backend/.env" ]; then
    cat > backend/.env << EOF
# AI DePIN Cloud Platform - Configuration

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG=True

# Storage
STORAGE_PATH=./sessions
CACHE_SIZE_MB=2048

# AI Models
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
DEEPSEEK_API_KEY=

# Game Settings
DEFAULT_FPS=60
DEFAULT_RESOLUTION=1920x1080
DEFAULT_GRAPHICS=ultra

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/platform.log
EOF
    print_success "تم إنشاء ملف .env"
else
    print_warning "ملف .env موجود بالفعل"
fi

# تحميل المتطلبات الإضافية
print_status "تحميل المتطلبات الإضافية..."

# FFmpeg (اختياري)
if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg غير مثبت (اختياري)"
    print_status "لتثبيت FFmpeg: apt-get install ffmpeg"
else
    print_success "FFmpeg موجود"
fi

# Tesseract (اختياري)
if ! command -v tesseract &> /dev/null; then
    print_warning "Tesseract غير مثبت (اختياري)"
    print_status "لتثبيت Tesseract: apt-get install tesseract-ocr"
else
    print_success "Tesseract موجود"
fi

# إنشاء سكريبت البدء
print_status "إنشاء سكريبت البدء..."
cat > start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
cd backend
python3 server.py
EOF
chmod +x start.sh
print_success "تم إنشاء سكريبت البدء"

# إنشاء سكريبت الاختبار
print_status "إنشاء سكريبت الاختبار..."
cat > test.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
cd backend
echo "اختبار الوكيل الذكي..."
python3 ai_agent.py
echo ""
echo "اختبار متحكم الألعاب..."
python3 game_controller.py
echo ""
echo "اختبار التخزين الكمي..."
python3 quantum_storage.py
echo ""
echo "اختبار مدير الجلسات..."
python3 session_manager.py
EOF
chmod +x test.sh
print_success "تم إنشاء سكريبت الاختبار"

# الملخص النهائي
echo ""
echo "=================================================="
echo -e "${GREEN}✅ تم التثبيت بنجاح!${NC}"
echo "=================================================="
echo ""
echo "📋 الخطوات التالية:"
echo ""
echo "1️⃣  تفعيل البيئة الافتراضية:"
echo "   source venv/bin/activate"
echo ""
echo "2️⃣  بدء السيرفر:"
echo "   ./start.sh"
echo "   أو"
echo "   cd backend && python3 server.py"
echo ""
echo "3️⃣  فتح الواجهة الأمامية:"
echo "   http://localhost:8080"
echo ""
echo "4️⃣  تشغيل الاختبارات:"
echo "   ./test.sh"
echo ""
echo "📚 الملفات المهمة:"
echo "   - frontend/index.html     (الواجهة الأمامية)"
echo "   - backend/server.py       (السيرفر الرئيسي)"
echo "   - backend/ai_agent.py     (الوكيل الذكي)"
echo "   - backend/game_controller.py (متحكم الألعاب)"
echo ""
echo "🎯 الميزات:"
echo "   ✨ 100% مجاني"
echo "   ⚡ سريع جداً"
echo "   🤖 ذكاء اصطناعي متقدم"
echo "   🎮 تشغيل الألعاب"
echo "   💾 تخزين كمي"
echo ""
echo "📞 للمساعدة: اقرأ README.md"
echo ""
