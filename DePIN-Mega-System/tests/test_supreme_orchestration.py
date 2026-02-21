import asyncio
import logging
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_supreme_orchestration_flow():
    print("🚀 Testing Supreme Multi-Agent Orchestration Flow (R1 + Llama)...")
    aoi = AOISystem()
    await aoi.initialize()
    
    # 1. التحقق من وجود القائد الأعلى
    commander = aoi.brain.supreme_commander
    print(f"👑 Supreme Commander Active: {commander is not None}")
    
    # 2. تشغيل هدف يتطلب تفكير عميق (Extreme Reasoning)
    print("🎯 Sending Extreme Goal to Supreme Control Node...")
    goal = "Design a decentralized AI protocol using quantum-resistant encryption across DePIN nodes."
    
    # نستخدم context خاص لتفعيل الـ Supreme Commander
    strategy = await aoi.brain.reason(goal, context={"extreme_reasoning": True})
    
    print(f"📊 Strategy Received from DeepSeek-R1: {strategy[:100]}...")
    
    # 3. جلب حالة الشبكة
    status = commander.get_cluster_status()
    print(f"📡 Cluster Status: {status['deepseek_p2p_nodes']} P2P nodes active.")
    print(f"💻 Local Load: {status['local_load']}")

    if "DeepSeek-R1" in strategy and status['deepseek_p2p_nodes'] >= 1000:
        print("✅ Supreme Orchestration test passed successfully!")
    else:
        print("❌ Supreme Orchestration test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_supreme_orchestration_flow())
