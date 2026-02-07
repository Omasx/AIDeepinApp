import asyncio
import logging
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_unified_ecosystem():
    print("🧪 Testing Unified Ecosystem Integration...")
    aoi = AOISystem()
    await aoi.initialize()

    # 1. اختبار وصول الوحدات الخارجية (ai_agent)
    print(f"📡 Motion Predictor Loaded: {aoi.predictor is not None}")

    # 2. اختبار وصول الوحدات الخارجية (decentralized_os)
    print(f"📦 Holographic Sharder Loaded: {aoi.sharder is not None}")

    # 3. اختبار تدفق AOI مع المكونات المدمجة
    print("🎯 Triggering Integrated Goal...")
    await aoi.trigger_goal("Audit system and shard sensitive data.")

    # التحقق من أن المهمة تمت وتسجلت
    history = aoi.memory.get_task_history()
    print(f"📊 Task History Count: {len(history)}")

    if len(history) > 0 and aoi.predictor and aoi.sharder:
        print("✅ Unified Ecosystem test passed successfully!")
    else:
        print("❌ Unified Ecosystem test failed or partially loaded.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_unified_ecosystem())
