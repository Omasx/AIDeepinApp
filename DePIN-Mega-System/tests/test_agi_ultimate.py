import asyncio
import logging
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_agi_ultimate_integration():
    print("🚀 Testing Ultimate AGI Integration...")
    aoi = AOISystem()
    await aoi.initialize()
    
    # 1. اختبار وصول الوكيل الفائق
    print(f"🧠 SuperIntelligentAgent Active: {aoi.brain.super_agent is not None}")
    
    # 2. اختبار المهام المعقدة للـ AGI
    print("🎯 Executing AGI Complex Task...")
    goal = "Create a cinematic video summary of the DePIN network"
    result = await aoi.brain.super_agent.execute_complex_task(goal, {"mode": "ultimate"})
    print(f"📊 AGI Task Success: {result['success']}")
    
    # 3. اختبار الصيانة الذاتية
    print("🔧 Testing Self-Maintenance...")
    m_result = await aoi.healing.maintenance.auto_optimize_performance()
    print(f"✅ Optimization Improvement: {m_result.get('improvement')}%")
    
    # 4. اختبار السحابة الكمية
    print("⚛️ Testing Quantum Cloud Storage...")
    q_result = await aoi.quantum_cloud.allocate_infinite_storage(1024) # 1TB
    print(f"📦 Compressed Size: {q_result.get('compressed_size_gb')} GB")

    if result['success'] and aoi.brain.super_agent and m_result['success']:
        print("✅ Ultimate AGI Ecosystem test passed successfully!")
    else:
        print("❌ Ultimate AGI Ecosystem test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_agi_ultimate_integration())
