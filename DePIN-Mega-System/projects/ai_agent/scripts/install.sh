#!/bin/bash

# install.sh - سكريبت التثبيت الشامل

echo "🚀 بدء تثبيت AI Agent Advanced..."

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    exit 1
fi

echo "✅ Python 3 موجود"

# إنشاء بيئة افتراضية
echo "📦 إنشاء بيئة افتراضية..."
python3 -m venv venv
source venv/bin/activate

# تحديث pip
echo "🔄 تحديث pip..."
pip install --upgrade pip setuptools wheel

# تثبيت المكاتب
echo "📥 تثبيت المكاتب المطلوبة..."
pip install -r backend/requirements.txt

# إنشاء ملف .env
echo "⚙️ إنشاء ملف .env..."
if [ ! -f .env ]; then
    cat > .env << EOF
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
GITHUB_TOKEN=your_github_token_here

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost/ai_agent

# Redis
REDIS_URL=redis://localhost:6379/0
EOF
    echo "✅ تم إنشاء ملف .env"
else
    echo "⚠️ ملف .env موجود بالفعل"
fi

echo "✅ انتهى التثبيت بنجاح!"
echo ""
echo "📝 الخطوات التالية:"
echo "1. عدّل ملف .env بمفاتيح API الخاصة بك"
echo "2. شغّل السيرفر: bash scripts/run.sh"
echo "3. افتح الواجهة الأمامية: http://localhost:8000"
