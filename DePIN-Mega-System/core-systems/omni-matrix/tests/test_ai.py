#!/usr/bin/env python3
"""
Tests for AI Dispatcher
"""

import asyncio
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ai_dispatcher import AIDispatcher, AIAgent, InferenceRequest


class MockOrchestrator:
    """Mock orchestrator for testing"""
    def __init__(self):
        self.config = {
            'ai': {
                'deepseek_r1_endpoint': 'https://api.deepseek.ai',
                'max_concurrent_agents': 100,
                'inference_timeout': 30,
                'fallback_models': ['gpt-4', 'claude-3']
            }
        }


@pytest.fixture
def ai_dispatcher():
    """Create test AI dispatcher"""
    mock_orch = MockOrchestrator()
    return AIDispatcher(mock_orch)


@pytest.mark.asyncio
async def test_agent_creation(ai_dispatcher):
    """Test agent creation"""
    await ai_dispatcher.initialize()
    
    # Check agents were created
    assert len(ai_dispatcher.agents) > 0
    
    # Check specializations
    assert 'general' in ai_dispatcher.agent_pools
    assert 'coding' in ai_dispatcher.agent_pools


@pytest.mark.asyncio
async def test_agent_selection(ai_dispatcher):
    """Test agent selection"""
    await ai_dispatcher.initialize()
    
    # Select agent
    agent = ai_dispatcher._select_agent('general')
    assert agent is not None
    assert agent.specialization == 'general'


@pytest.mark.asyncio
async def test_inference_request_creation():
    """Test inference request creation"""
    request = InferenceRequest(
        request_id='test-123',
        prompt='Hello, world!',
        model='deepseek-r1-641b',
        max_tokens=100,
        temperature=0.7,
        priority=5
    )
    
    assert request.request_id == 'test-123'
    assert request.prompt == 'Hello, world!'
    assert request.model == 'deepseek-r1-641b'


@pytest.mark.asyncio
async def test_agent_swarm_creation(ai_dispatcher):
    """Test agent swarm creation"""
    await ai_dispatcher.initialize()
    
    agent_ids = await ai_dispatcher.create_agent_swarm(
        count=10,
        specialization='coding',
        model='deepseek-r1-641b'
    )
    
    assert len(agent_ids) == 10
    assert 'coding' in ai_dispatcher.agent_pools


@pytest.mark.asyncio
async def test_agent_status(ai_dispatcher):
    """Test agent status reporting"""
    await ai_dispatcher.initialize()
    
    status = await ai_dispatcher.get_agent_status()
    
    assert 'total_agents' in status
    assert 'idle' in status
    assert 'busy' in status
    assert 'specializations' in status


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
