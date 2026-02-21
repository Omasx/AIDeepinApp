import unittest
import asyncio
from projects.decentralized_os.storage.holographic_sharding import BekensteinSharder
from projects.decentralized_os.core.deos_orchestrator import VirtualChipOrchestrator
from projects.decentralized_os.economy.barter_system import BarterValidator

class TestDeOS(unittest.TestCase):
    
    def test_sharding_logic(self):
        sharder = BekensteinSharder()
        data = b"Some distributed data for testing"
        shards = sharder.generate_shards(data, num_nodes=2)
        self.assertGreater(len(shards), 0)
        self.assertEqual(shards[0]["id"], 0)
        
    def test_barter_system(self):
        validator = BarterValidator("TEST_WALLET")
        validator.start_validation()
        reward = validator.perform_validation_task()
        self.assertGreaterEqual(reward, 0)
        self.assertGreater(validator.get_balance(), 0)

    def test_orchestrator_status(self):
        orchestrator = VirtualChipOrchestrator()
        loop = asyncio.get_event_loop()
        status = loop.run_until_complete(orchestrator.get_system_status())
        self.assertEqual(status["active_tasks"], 0)
        self.assertIn("TFLOPS", status["compute_capacity"])

if __name__ == "__main__":
    unittest.main()
