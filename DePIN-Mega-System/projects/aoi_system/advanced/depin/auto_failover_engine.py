import asyncio
from typing import Dict, List, Any, Optional, Callable
import logging
from datetime import datetime

logger = logging.getLogger("AOI-DePIN-Failover")

class AutoFailoverEngine:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.failover_events = []

    async def execute_with_failover(
        self,
        task_id: str,
        task_type: str,
        requirements: Any,
        execution_func: Callable
    ) -> Dict[str, Any]:
        logger.info(f"🎯 Executing task {task_id} with Auto-Failover...")
        
        # Try primary providers
        providers = list(self.orchestrator.providers.values())
        
        for i, status in enumerate(providers):
            provider = status.provider
            try:
                logger.info(f"  🔄 Attempt {i+1} on {provider.value}")
                result = await asyncio.wait_for(execution_func(provider, requirements), timeout=10)
                return {"success": True, "result": result, "provider": provider.value}
            except Exception as e:
                logger.warning(f"  ❌ Failed on {provider.value}: {e}")
                self.failover_events.append({"task_id": task_id, "from": provider.value, "timestamp": datetime.now()})
                continue
        
        return {"success": False, "error": "All providers failed"}
