import unittest
import asyncio
from projects.decentralized_os.agi.agi_brain import AGIBrain
from projects.decentralized_os.agi.key_battery import KeyBatteryManager
from projects.decentralized_os.agi.media_alchemy import MediaAlchemy

class TestAGIEnhanced(unittest.TestCase):
    
    def test_brain_learning(self):
        brain = AGIBrain()
        initial_rate = brain.tool_success_rates.get("media_processor", 0.7)
        brain.record_outcome("media_processor", True)
        new_rate = brain.tool_success_rates.get("media_processor")
        self.assertGreater(new_rate, initial_rate)

    def test_key_rotation(self):
        manager = KeyBatteryManager()
        key1 = manager.get_fresh_key("openai")
        key2 = manager.report_failure("openai", 429)
        self.assertNotEqual(key1, key2)

    def test_media_production(self):
        alchemy = MediaAlchemy()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(alchemy.create_video("Test", [], "test.mp4"))
        self.assertIn("exports/test.mp4", result["path"])

if __name__ == "__main__":
    unittest.main()
