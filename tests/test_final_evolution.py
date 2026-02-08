import asyncio
import logging
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_final_evolution_v2():
    print("🚀 Testing Final Evolution V2 Integration...")
    aoi = AOISystem()
    await aoi.initialize()

    # 1. اختبار Llama Cloud
    print("🧠 Initializing Llama Cloud...")
    l_res = await aoi.llama_cloud.initialize_on_login({"email": "test@aidepin.app"})
    print(f"✅ Llama Cloud Status: {l_res['status']}")

    # 2. اختبار الشبكة الاجتماعية
    print("🌐 Creating Social Post...")
    s_res = await aoi.social.create_post("test_user", "Hello DePIN World!", "post")
    print(f"✅ Social Post ID: {s_res['post_id']}")

    # 3. اختبار البلوكشين
    print("⛓️ Switching Blockchain...")
    b_res = await aoi.blockchain.switch_network("solana")
    print(f"✅ Active Network: {b_res['active_network']}")

    # 4. اختبار التوسيع
    print("📊 Handling Massive Scale...")
    p_res = await aoi.scaler.handle_massive_scale(1000000)
    print(f"✅ Latency at 1M users: {p_res['latency_ms']}ms")

    if l_res['success'] and s_res['success'] and b_res['success']:
        print("🎉 Final Evolution V2 test passed successfully!")
    else:
        print("❌ Final Evolution V2 test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_final_evolution_v2())
