import asyncio
import logging
import sys
import os
from datetime import datetime, timedelta

# إضافة المسار الحالي لتمكين الاستيراد
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_scheduler_concurrency():
    print("🚀 Starting Scheduler Concurrency Test...")
    aoi = AOISystem()
    await aoi.initialize()

    # جدولة مهمتين في نفس الوقت (بعد 5 ثواني)
    run_time = datetime.now() + timedelta(seconds=5)
    
    print(f"📅 Scheduling two tasks for {run_time}")
    
    await aoi.schedule_new_task("Security Audit", "Perform security check", "System", run_time)
    await aoi.schedule_new_task("Data Backup", "Backup user data", "Data", run_time)

    print("⏳ Waiting for tasks to trigger...")
    await asyncio.sleep(15) # انتظر حتى يتم التنفيذ
    
    # التحقق من الذاكرة
    history = aoi.memory.get_task_history()
    print(f"📊 Task History Count: {len(history)}")
    
    for h in history:
        print(f"✅ Executed: {h['description']}")

    if len(history) >= 2:
        print("✅ Scheduler Concurrency test passed!")
    else:
        print("❌ Scheduler test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_scheduler_concurrency())
