"""Tests for Agent Behaviors and Multi-Agent Cooperation."""

import pytest
from simlab.agents import CoordinatorAgent, WorkerAgent, CriticAgent
from simlab.core.bus import MessageBus
from simlab.core.logging import CausalEventLogger
from simlab.core.state import EnvironmentState


def test_coordinator_delegation():
    coord = CoordinatorAgent(agent_id="coord", managed_workers=["w1"])
    state = {
        "tasks": [{"task_id": "t1", "status": "PENDING"}],
        "budget": 100
    }

    obs = coord.observe(state, incoming_messages=[], current_tick=0)
    action = coord.decide(obs, current_tick=0)

    assert action.action_type == "SEND_MESSAGE"
    assert action.target == "w1"
    assert action.parameters["content"]["type"] == "ASSIGN_TASK"


def test_worker_accept_and_submit():
    worker = WorkerAgent(agent_id="w1", critic_id="critic_01")
    state = EnvironmentState({"energy": 100})
    bus = MessageBus()
    logger = CausalEventLogger()

    # 1. Deliver task assignment message
    bus.register_agent("w1")
    bus.register_agent("critic_01")
    bus.send("coord", "w1", {"type": "ASSIGN_TASK", "task": {"task_id": "t1"}}, current_tick=0)
    msgs = bus.deliver_in_flight(current_tick=0)
    incoming = bus.receive("w1")

    # Worker perceives and accepts
    act1 = worker.step(0, state, incoming, bus, logger)
    assert act1.action_type == "ACCEPT_TASK"

    # Worker executes task
    act2 = worker.step(1, state, [], bus, logger)
    assert act2.action_type == "EXECUTE_TASK"

    # Worker submits to critic
    act3 = worker.step(2, state, [], bus, logger)
    assert act3.action_type == "SUBMIT_FOR_REVIEW"
    assert act3.target == "critic_01"


def test_critic_approval_and_rejection():
    critic = CriticAgent(agent_id="critic")
    state = {"state_hash": "abc"}

    # Mock submission
    class MockMsg:
        sender_id = "w1"
        content = {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": "t1",
            "submission": {"result_value": 42}
        }
        sent_tick = 1

    obs = critic.observe(state, incoming_messages=[MockMsg()], current_tick=2)
    action = critic.decide(obs, current_tick=2)
    assert action.action_type == "APPROVE_TASK"
    assert action.parameters["verdict"] == "APPROVED"

    # Mock corrupted submission
    class BadMsg:
        sender_id = "w1"
        content = {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": "t2",
            "submission": {"result_value": -99}
        }
        sent_tick = 1

    obs_bad = critic.observe(state, incoming_messages=[BadMsg()], current_tick=2)
    action_bad = critic.decide(obs_bad, current_tick=2)
    assert action_bad.action_type == "SEND_MESSAGE"
    assert action_bad.parameters["content"]["verdict"] == "REJECTED"
