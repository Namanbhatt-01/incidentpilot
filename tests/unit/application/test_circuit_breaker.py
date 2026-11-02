from __future__ import annotations

import pytest

from packages.application.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError


def test_circuit_breaker_closed_normal_execution() -> None:
    breaker = CircuitBreaker(failure_threshold=3, recovery_time=10.0)
    result = breaker.call(lambda x: x * 2, 5)
    assert result == 10
    assert breaker.state == "CLOSED"


def test_circuit_breaker_trips_to_open_after_threshold() -> None:
    breaker = CircuitBreaker(failure_threshold=3, recovery_time=10.0)

    def failing_call() -> None:
        raise RuntimeError("LLM timeout")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.call(failing_call)

    assert breaker.state == "OPEN"
    # Next call fails fast without invoking target
    with pytest.raises(CircuitBreakerOpenError) as exc_info:
        breaker.call(failing_call)
    assert "Circuit breaker is OPEN" in str(exc_info.value)
