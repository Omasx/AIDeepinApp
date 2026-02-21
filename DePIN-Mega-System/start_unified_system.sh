#!/bin/bash
# start_unified_system.sh - المُشغل الموحد لنظام AOI و DeOS

echo "🚀 Starting AOI Unified Ecosystem..."

# تحديد المسار الجذري
export PYTHONPATH=$PYTHONPATH:.

# التأكد من وجود المجلدات المطلوبة
mkdir -p projects/aoi_system/data
mkdir -p projects/aoi_system/logs

# تشغيل السيرفر الموحد في الخلفية
echo "🌐 Launching Unified Backend Server on port 8000..."
python3 projects/aoi_system/unified_server.py &
SERVER_PID=$!

# انتظر قليلاً لضمان بدء السيرفر
sleep 5

# عرض الحالة الأولية
echo "📊 Checking System Status..."
curl -s http://localhost:8000/api/status | python3 -m json.tool

echo "✅ Ecosystem is now running."
echo "Press Ctrl+C to stop."

# انتظار السيرفر
wait $SERVER_PID
