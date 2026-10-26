"""Base Agent Interface and Lifecycle Abstractions."""

from abc import ABC, abstractmethod
import copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class AgentAction:
    """Action emitted by an agent during its decision cycle."""
    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract Base Class for all SimLab agents."""

    def __init__(
        self,
        agent_id: str,
        role: str,
        capabilities: Optional[List[str]] = None,
        objectives: Optional[List[str]] = None,
        max_working_memory: int = 20
    ):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = list(capabilities or [])
        self.objectives = list(objectives or [])
        self.max_working_memory = max(1, max_working_memory)

        self._working_memory: List[Dict[str, Any]] = []
        self._decision_traces: List[Dict[str, Any]] = []
        self._is_active: bool = True

    @property
    def is_active(self) -> bool:
        """Whether agent is currently enabled in simulation."""
        return self._is_active

    def set_active(self, active: bool) -> None:
        """Enable or disable agent."""
        self._is_active = active

    def add_memory(self, item: Dict[str, Any], tick: int) -> None:
        """Add an item to working memory with bounded FIFO eviction."""
        record = dict(item)
        record["tick"] = tick
        self._working_memory.append(record)
        if len(self._working_memory) > self.max_working_memory:
            self._working_memory.pop(0)

    def get_working_memory(self) -> List[Dict[str, Any]]:
        """Retrieve current bounded working memory."""
        return list(self._working_memory)

    @property
    def memory(self) -> Any:
        """Convenience property for working memory access."""
        class _WorkingMemoryAccessor:
            def __init__(accessor_self, agent_instance):
                accessor_self._agent = agent_instance
            @property
            def size(accessor_self) -> int:
                return len(accessor_self._agent._working_memory)
            def __len__(accessor_self) -> int:
                return len(accessor_self._agent._working_memory)
            def to_list(accessor_self) -> List[Dict[str, Any]]:
                return list(accessor_self._agent._working_memory)
        return _WorkingMemoryAccessor(self)

    def get_decision_traces(self) -> List[Dict[str, Any]]:
        """Retrieve historical decision traces."""
        return list(self._decision_traces)

    @abstractmethod
    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Filter environmental state and incoming messages into agent observation."""
        pass

    @abstractmethod
    def decide(self, observation: Dict[str, Any], current_tick: int) -> AgentAction:
        """Evaluate observation and return an action according to agent policy."""
        pass

    def record_decision_trace(self, tick: int, observation: Dict[str, Any], action: AgentAction) -> None:
        """Store structured decision trace."""
        trace = {
            "tick": tick,
            "agent_id": self.agent_id,
            "role": self.role,
            "observation_summary": {k: type(v).__name__ for k, v in observation.items()},
            "action_type": action.action_type,
            "target": action.target,
            "rationale": action.rationale,
            "parameters": copy.deepcopy(action.parameters),
        }
        self._decision_traces.append(trace)

    def step(
        self,
        current_tick: int,
        environment_state: Any,
        incoming_messages: List[Any],
        bus: Any,
        logger: Any
    ) -> Optional[AgentAction]:
        """Execute one complete perceive-decide-act cycle."""
        if not self._is_active:
            return None

        # 1. Observe
        obs = self.observe(environment_state.to_dict(), incoming_messages, current_tick)
        self.add_memory({"type": "observation", "summary": obs.get("summary", "tick_observation")}, current_tick)

        # 2. Decide
        action = self.decide(obs, current_tick)
        self.record_decision_trace(current_tick, obs, action)

        # 3. Log event
        if logger:
            logger.log_event(
                tick=current_tick,
                actor_id=self.agent_id,
                action=action.action_type,
                inputs={"parameters": action.parameters, "target": action.target},
                outcome={"rationale": action.rationale},
                event_type="AGENT_DECISION"
            )

        return action

    def snapshot(self) -> Dict[str, Any]:
        """Create serializable agent snapshot."""
        return {
            "version": 1,
            "agent_id": self.agent_id,
            "role": self.role,
            "capabilities": list(self.capabilities),
            "objectives": list(self.objectives),
            "is_active": self._is_active,
            "working_memory": [dict(m) for m in self._working_memory],
            "decision_traces": [dict(t) for t in self._decision_traces],
            "decision_traces_count": len(self._decision_traces),
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore agent state."""
        if not isinstance(data, dict):
            raise ValueError(f"Agent snapshot must be a dict, got {type(data).__name__}")
        if "is_active" not in data or "working_memory" not in data:
            raise ValueError("Malformed agent snapshot: missing required fields 'is_active' or 'working_memory'")
        if not isinstance(data["working_memory"], list):
            raise ValueError("Malformed agent snapshot: 'working_memory' must be a list")

        self._is_active = bool(data["is_active"])
        self._working_memory = [dict(m) for m in data["working_memory"]]

        if "decision_traces" in data:
            raw_traces = data["decision_traces"]
            if not isinstance(raw_traces, list):
                raise ValueError("Malformed agent snapshot: 'decision_traces' must be a list")
            validated = []
            for item in raw_traces:
                if not isinstance(item, dict):
                    raise ValueError("Malformed agent snapshot: decision trace entry must be a dict")
                validated.append(dict(item))
            if "decision_traces_count" in data:
                count = data["decision_traces_count"]
                if not isinstance(count, int) or count != len(validated):
                    raise ValueError(
                        f"Malformed agent snapshot: decision_traces_count ({count}) does not match len(decision_traces) ({len(validated)})"
                    )
            self._decision_traces = validated
        else:
            self._decision_traces = []
