#!/bin/bash

# run.sh - سكريبت تشغيل السيرفر

echo "🚀 بدء تشغيل AI Agent Advanced..."

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تحميل متغيرات البيئة
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# التحقق من المكاتب المطلوبة
echo "✅ التحقق من المكاتب..."

# تشغيل السيرفر
echo "🌐 تشغيل السيرفر على http://0.0.0.0:8000"
echo ""
echo "📊 الواجهة الأمامية: http://localhost:8000"
echo "📚 API: http://localhost:8000/api"
echo ""
echo "اضغط Ctrl+C لإيقاف السيرفر"
echo ""

cd backend
python3 server.py
