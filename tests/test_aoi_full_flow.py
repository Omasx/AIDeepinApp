import asyncio
import logging
import sys
import os

# إضافة المسار الحالي لتمكين الاستيراد
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_full_system_flow():
    """
    اختبار تدفق النظام الكامل عبر الطبقات الـ 9.
    """
    print("🚀 Starting Full AOI System Test...")
    aoi = AOISystem()

    # تهيئة النظام
    await aoi.initialize()

    # محاكاة إعطاء هدف معقد
    goal = "Perform a full system security audit and optimize storage."

    # تشغيل التدفق (التفكير -> التخطيط -> التنفيذ -> المراقبة)
    print(f"🎯 Triggering Goal: {goal}")
    test_task = asyncio.create_task(aoi.trigger_goal(goal))

    # انتظر قليلاً للمراقبة
    for _ in range(5):
        status = await aoi.get_realtime_status()
        print(f"📊 Real-time Status: State={status['state']}, CPU={status['resources']['cpu']}%")
        await asyncio.sleep(2)

    await test_task
    print("✅ Full system flow test completed successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_full_system_flow())
