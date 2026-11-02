from __future__ import annotations

from packages.domain.events import IncidentState


class IllegalStateTransitionError(ValueError):
    """Raised when an incident attempts an invalid lifecycle state transition."""

    pass


class IncidentStateMachine:
    """Finite State Machine guarding the incident lifecycle transitions."""

    # Explicit allowed transition matrix
    _TRANSITIONS: dict[IncidentState, set[IncidentState]] = {
        IncidentState.DETECTED: {IncidentState.TRIAGED, IncidentState.ABORTED},
        IncidentState.TRIAGED: {IncidentState.INVESTIGATING, IncidentState.ABORTED},
        IncidentState.INVESTIGATING: {IncidentState.REPRODUCING, IncidentState.ABORTED},
        IncidentState.REPRODUCING: {
            IncidentState.CRITIC_REVIEW,
            IncidentState.INVESTIGATING,
            IncidentState.ABORTED,
        },
        IncidentState.CRITIC_REVIEW: {
            IncidentState.AWAITING_APPROVAL,
            IncidentState.INVESTIGATING,
            IncidentState.ABORTED,
        },
        IncidentState.AWAITING_APPROVAL: {
            IncidentState.REMEDIATING,
            IncidentState.INVESTIGATING,
            IncidentState.ABORTED,
        },
        IncidentState.REMEDIATING: {IncidentState.VERIFYING, IncidentState.ABORTED},
        IncidentState.VERIFYING: {
            IncidentState.RESOLVED,
            IncidentState.INVESTIGATING,
            IncidentState.ABORTED,
        },
        IncidentState.RESOLVED: set(),
        IncidentState.ABORTED: set(),
    }

    def __init__(self, initial_state: IncidentState = IncidentState.DETECTED) -> None:
        self._state: IncidentState = initial_state

    @property
    def current_state(self) -> IncidentState:
        return self._state

    def can_transition_to(self, target_state: IncidentState) -> bool:
        return target_state in self._TRANSITIONS.get(self._state, set())

    def transition_to(self, target_state: IncidentState) -> None:
        if not self.can_transition_to(target_state):
            raise IllegalStateTransitionError(
                f"Illegal transition from {self._state.value} to {target_state.value}"
            )
        self._state = target_state
