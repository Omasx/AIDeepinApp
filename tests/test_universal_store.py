import asyncio
import logging
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_universal_store_and_gui_agent():
    print("🚀 Testing Universal Store and GUI Agent...")
    aoi = AOISystem()
    await aoi.initialize()

    # 1. اختبار قائمة المتاجر
    stores = aoi.store.list_all_stores()
    print(f"🏬 Total Stores in Registry: {len(stores)}")

    # 2. اختبار تثبيت تطبيق
    print("📥 Installing App: 'Call of Duty' from 'Steam'...")
    install_res = await aoi.app_bridge.install_app("Call of Duty", "steam", "Windows")
    app_id = install_res['app_id']
    print(f"✅ App Installed. ID: {app_id}")

    # 3. اختبار تشغيل مهمة GUI (Mouse/Keyboard Agency)
    print("🖱️ Triggering AI Mission: 'Win a match and send GG'...")
    mission_res = await aoi.gui_agent.execute_gui_mission(app_id, "Win a match and send GG")
    print(f"📊 Mission Status: {mission_res['status']}")

    # 4. اختبار طلب الموافقة
    print("⏳ Submitting results for human approval...")
    task_id = "test_task_001"
    await aoi.control.submit_for_approval(task_id, mission_res['results'])
    print(f"📡 System State: {aoi.control.state.value}")

    # 5. محاكاة الموافقة والمزامنة
    print("✅ Approving mission results...")
    await aoi.control.approve_task(task_id)
    print(f"🏁 Final System State: {aoi.control.state.value}")

    if len(stores) >= 90 and install_res['success'] and mission_res['success']:
        print("🎉 Universal Store Ecosystem test passed successfully!")
    else:
        print("❌ Universal Store Ecosystem test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_universal_store_and_gui_agent())
