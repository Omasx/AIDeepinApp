#!/bin/bash

# test.sh - سكريبت الاختبار الشامل

echo "🧪 بدء الاختبارات..."

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تشغيل الاختبارات
echo "✅ تشغيل اختبارات الوحدة..."
cd backend
python3 -m pytest tests/ -v --cov=advanced_agent --cov=depin_network

echo ""
echo "✅ انتهت الاختبارات!"
