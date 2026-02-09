#!/usr/bin/env python3
"""
Tests for Storage Sharder
"""

import asyncio
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.storage_sharder import ErasureCoder, StorageSharder


class MockOrchestrator:
    """Mock orchestrator for testing"""
    def __init__(self):
        self.config = {
            'storage': {
                'total_capacity_tb': 50,
                'redundancy_factor': 3,
                'shard_size_mb': 64,
                'erasure_coding': True,
                'data_shards': 4,
                'parity_shards': 2
            }
        }


@pytest.fixture
def erasure_coder():
    """Create test erasure coder"""
    return ErasureCoder(data_shards=4, parity_shards=2)


@pytest.fixture
def storage_sharder():
    """Create test storage sharder"""
    mock_orch = MockOrchestrator()
    return StorageSharder(mock_orch)


def test_erasure_coding_encode_decode(erasure_coder):
    """Test erasure coding encode/decode"""
    original_data = b"Hello, World! This is test data for erasure coding."
    
    # Encode
    shards = erasure_coder.encode(original_data)
    assert len(shards) == 6  # 4 data + 2 parity
    
    # Decode with all shards
    decoded = erasure_coder.decode(shards, len(shards[0]))
    assert decoded == original_data


def test_erasure_coding_with_loss(erasure_coder):
    """Test erasure coding with shard loss"""
    original_data = b"Test data for shard loss recovery."
    
    # Encode
    shards = erasure_coder.encode(original_data)
    
    # Simulate loss of 1 data shard and 1 parity shard
    shards[0] = None
    shards[4] = None
    
    # Should still decode
    decoded = erasure_coder.decode(shards, len(shards[1]))
    assert decoded == original_data


@pytest.mark.asyncio
async def test_storage_stats(storage_sharder):
    """Test storage statistics"""
    stats = storage_sharder.get_storage_stats()
    
    assert 'total_objects' in stats
    assert 'total_stored_bytes' in stats
    assert 'shard_count' in stats


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
