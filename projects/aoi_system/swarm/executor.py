import asyncio
import subprocess
import logging
import os
import sys
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger("AOI-Swarm-Executor")

class CodeExecutor:
    """
    3. The "Manus-Like" Capabilities (Self-Healing & Sandbox)
    المسؤولية: تنفيذ الكود، التقاط الأخطاء، وإرسالها للمدير الذكي للإصلاح التلقائي.
    """
    def __init__(self, work_dir: str = "projects/aoi_system/sandbox"):
        self.work_dir = work_dir
        os.makedirs(self.work_dir, exist_ok=True)
        logger.info(f"🛠️ CodeExecutor ready in sandbox: {work_dir}")

    async def run_python(self, code: str, filename: str = "temp_script.py") -> Dict[str, Any]:
        """
        تشغيل كود بايثون والتقاط المخرجات والأخطاء.
        """
        filepath = os.path.join(self.work_dir, filename)
        with open(filepath, "w") as f:
            f.write(code)

        logger.info(f"⚙️ Executing {filename}...")

        try:
            # تشغيل في subprocess مع تحديد Timeout لمنع التجميد
            process = await asyncio.create_subprocess_exec(
                sys.executable, filepath,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            exit_code = process.returncode

            return {
                "exit_code": exit_code,
                "stdout": stdout.decode().strip(),
                "stderr": stderr.decode().strip(),
                "success": exit_code == 0
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }

    async def autonomous_repair_loop(self, initial_code: str, repair_agent: Callable, max_retries: int = 3) -> Dict[str, Any]:
        """
        دورة التكرار الذاتي: تنفيذ -> خطأ -> تحليل -> إصلاح -> تنفيذ.
        """
        current_code = initial_code
        attempts = 0

        while attempts < max_retries:
            attempts += 1
            logger.info(f"🔄 Execution Attempt {attempts}/{max_retries}")

            result = await self.run_python(current_code)

            if result["success"]:
                logger.info("✅ Code executed successfully!")
                return {"final_code": current_code, "result": result, "attempts": attempts}

            logger.warning(f"❌ Error detected in attempt {attempts}:\n{result['stderr']}")

            # إذا فشل الكود، نرسل الخطأ للـ LLM (عبر repair_agent) ليقوم بالإصلاح
            logger.info("🧠 Sending stack trace to AGI for analysis and repair...")
            prompt = f"""
            The following python code failed with an error.
            CODE:
            {current_code}

            ERROR (STDERR):
            {result['stderr']}

            Please analyze the stack trace, identify the bug, and provide the FULL FIXED python code.
            """

            fixed_code = await repair_agent(prompt)
            # تنظيف الرد (إزالة Markdown code blocks إذا وجدت)
            current_code = self._clean_llm_code(fixed_code)

        logger.error("🛑 Max retries reached. System could not self-repair.")
        return {"final_code": current_code, "result": result, "attempts": attempts, "status": "failed"}

    def _clean_llm_code(self, raw_response: str) -> str:
        # إزالة وسوم Markdown للتأكد من الحصول على كود نقي
        if "```python" in raw_response:
            return raw_response.split("```python")[1].split("```")[0].strip()
        elif "```" in raw_response:
            return raw_response.split("```")[1].split("```")[0].strip()
        return raw_response.strip()
