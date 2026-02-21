# live_executor.py
import logging

logger = logging.getLogger(__name__)

class LiveAgentExecutor:
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager
        self.agi_agent = None

    async def execute_live(self, task: str, user_id: str):
        logger.info(f"Executing live task for {user_id}: {task}")
        if self.agi_agent:
            return await self.agi_agent.execute_complex_task(task, {"user_id": user_id})
        return {"error": "AGI Agent not linked"}
