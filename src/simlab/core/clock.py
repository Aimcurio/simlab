"""Deterministic Simulation Clock."""

from typing import Dict, Any


class SimulationClock:
    """Manages virtual discrete time for simulation runs."""

    def __init__(self, tick_duration_seconds: float = 1.0, initial_tick: int = 0):
        self.tick_duration_seconds = max(0.0001, tick_duration_seconds)
        self._current_tick = initial_tick
        self._initial_tick = initial_tick

    @property
    def current_tick(self) -> int:
        """Current discrete simulation tick."""
        return self._current_tick

    @property
    def virtual_time_seconds(self) -> float:
        """Elapsed virtual simulation time in seconds."""
        return self._current_tick * self.tick_duration_seconds

    def advance(self, ticks: int = 1) -> int:
        """Advance the clock by a specified number of ticks."""
        if ticks < 0:
            raise ValueError(f"Cannot advance clock by negative ticks: {ticks}")
        self._current_tick += ticks
        return self._current_tick

    def reset(self) -> None:
        """Reset the clock back to initial tick."""
        self._current_tick = self._initial_tick

    def snapshot(self) -> Dict[str, Any]:
        """Capture clock state snapshot."""
        return {
            "current_tick": self._current_tick,
            "tick_duration_seconds": self.tick_duration_seconds,
            "initial_tick": self._initial_tick
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore clock state from snapshot."""
        self._current_tick = data["current_tick"]
        self.tick_duration_seconds = data["tick_duration_seconds"]
        self._initial_tick = data.get("initial_tick", 0)

    def __repr__(self) -> str:
        return f"SimulationClock(tick={self._current_tick}, virtual_time={self.virtual_time_seconds:.2f}s)"


# Alias
DiscreteClock = SimulationClock

