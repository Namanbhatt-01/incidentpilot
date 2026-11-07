from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


class CircuitBreakerOpenError(RuntimeError):
    """Raised when an operation is attempted while circuit breaker is OPEN."""

    pass


class CircuitBreaker:
    """Token-bucket style circuit breaker guarding external LLM and tool calls."""

    def __init__(self, failure_threshold: int = 3, recovery_time: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = 0.0
        self._state = "CLOSED"

    @property
    def state(self) -> str:
        if self._state == "OPEN" and time.time() - self.last_failure_time > self.recovery_time:
            self._state = "HALF_OPEN"
        return self._state

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        current_state = self.state
        if current_state == "OPEN":
            raise CircuitBreakerOpenError(
                "Circuit breaker is OPEN. Fast failing request to protect upstream systems."
            )

        try:
            result = func(*args, **kwargs)
            if self._state == "HALF_OPEN":
                self.reset()
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self._state == "HALF_OPEN" or self.failure_count >= self.failure_threshold:
                self._state = "OPEN"
            raise

    def reset(self) -> None:
        self.failure_count = 0
        self._state = "CLOSED"
