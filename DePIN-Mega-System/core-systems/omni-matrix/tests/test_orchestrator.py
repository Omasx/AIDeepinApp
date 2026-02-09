#!/usr/bin/env python3
"""
Tests for Omni-Matrix Orchestrator
"""

import asyncio
import pytest
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import OmniMatrixOrchestrator, get_orchestrator


@pytest.fixture
def orchestrator():
    """Create test orchestrator"""
    return get_orchestrator()


@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Test orchestrator initialization"""
    assert orchestrator is not None
    assert orchestrator.instance_id is not None
    assert orchestrator.state.value == 'initializing'


@pytest.mark.asyncio
async def test_config_loading(orchestrator):
    """Test configuration loading"""
    assert orchestrator.config is not None
    assert 'networks' in orchestrator.config
    assert 'ai' in orchestrator.config
    assert 'storage' in orchestrator.config


@pytest.mark.asyncio
async def test_task_submission(orchestrator):
    """Test task submission"""
    task_id = await orchestrator.submit_task(
        'ai_inference',
        {'prompt': 'Hello, world!'},
        priority=5
    )
    
    assert task_id is not None
    assert len(task_id) > 0


@pytest.mark.asyncio
async def test_status_reporting(orchestrator):
    """Test status reporting"""
    status = orchestrator.get_status()
    
    assert 'instance_id' in status
    assert 'state' in status
    assert 'nodes' in status
    assert 'tasks' in status


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
