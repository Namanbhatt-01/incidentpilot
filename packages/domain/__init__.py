"""Domain layer: pure business models, state machines, events, and invariants."""

from packages.domain.digest import ActionDigest
from packages.domain.events import (
    DomainEvent,
    HumanApprovalGrantedEvent,
    IncidentDetectedEvent,
    IncidentState,
    ReproductionConfirmedEvent,
)
from packages.domain.fsm import IllegalStateTransitionError, IncidentStateMachine

__all__ = [
    "ActionDigest",
    "DomainEvent",
    "HumanApprovalGrantedEvent",
    "IllegalStateTransitionError",
    "IncidentDetectedEvent",
    "IncidentState",
    "IncidentStateMachine",
    "ReproductionConfirmedEvent",
]
