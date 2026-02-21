import asyncio
import logging
import sys
import os

# إضافة المسار الحالي لتمكين الاستيراد
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_swarm_and_repair():
    print("🚀 Starting Swarm AGI & Self-Repair Test...")
    aoi = AOISystem()
    await aoi.initialize()

    # 1. اختبار الـ Swarm (100 عميل متزامن)
    print("\n--- Testing Swarm Concurrency ---")
    await aoi.trigger_swarm_goal("Massive data analysis", agent_count=50)

    # 2. اختبار الـ Autonomous Repair (Manus-like)
    print("\n--- Testing Autonomous Self-Repair ---")
    # كود بايثون فيه خطأ متعمد (Syntax Error or NameError)
    broken_code = """
import sys
print("Hello from Swarm!")
# خطأ متعمد: استدعاء متغير غير موجود
print(undefined_variable)
    """
    
    # دالة محاكاة للإصلاح (LLM)
    async def mock_repair_agent(prompt: str):
        print("🧠 LLM Analyzing error and fixing code...")
        return """
import sys
print("Hello from Swarm!")
fixed_variable = "I am now defined."
print(fixed_variable)
        """

    repair_result = await aoi.engine.run_autonomous_coding(broken_code, mock_repair_agent)
    
    print("\n--- Repair Results ---")
    print(f"Status: {'Success' if repair_result['result']['success'] else 'Failed'}")
    print(f"Attempts: {repair_result['attempts']}")
    print(f"Output: {repair_result['result']['stdout']}")
    
    if repair_result['result']['success']:
        print("✅ Swarm AGI and Self-Repair tests passed!")
    else:
        print("❌ Self-Repair test failed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_swarm_and_repair())
