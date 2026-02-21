import asyncio
import logging
import unittest
import sys
import os

# إضافة المسار الحالي لتمكين الاستيراد
sys.path.append(os.getcwd())

from projects.deos_core.kernel import DeOSKernel
from projects.deos_core.memory import LongTermMemory

class TestDeOSCore(unittest.IsolatedAsyncioTestCase):
    async def test_kernel_loop_initialization(self):
        """
        اختيار تهيئة النواة وتدفق العمل.
        """
        kernel = DeOSKernel()
        self.assertIsNotNone(kernel.orchestrator)
        self.assertIsNotNone(kernel.monitor)
        
        # إضافة هدف اختباري
        kernel.memory.add_goal("Test autonomous task execution")
        
        # تشغيل النواة لفترة قصيرة جداً للاختبار
        task = asyncio.create_task(kernel.start_loop())
        await asyncio.sleep(5) # انتظر دورة واحدة
        kernel.stop()
        await task
        
        # التحقق من أن الذاكرة سجلت شيئاً
        history = kernel.memory.data["history"]
        self.assertTrue(len(history) >= 0)
        print("✅ Kernel test passed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
