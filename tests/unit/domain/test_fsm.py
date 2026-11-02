from __future__ import annotations

import pytest

from packages.domain.events import IncidentState
from packages.domain.fsm import IllegalStateTransitionError, IncidentStateMachine


def test_fsm_initial_state() -> None:
    fsm = IncidentStateMachine(initial_state=IncidentState.DETECTED)
    assert fsm.current_state == IncidentState.DETECTED


def test_fsm_valid_full_lifecycle() -> None:
    fsm = IncidentStateMachine(initial_state=IncidentState.DETECTED)
    fsm.transition_to(IncidentState.TRIAGED)
    fsm.transition_to(IncidentState.INVESTIGATING)
    fsm.transition_to(IncidentState.REPRODUCING)
    fsm.transition_to(IncidentState.CRITIC_REVIEW)
    fsm.transition_to(IncidentState.AWAITING_APPROVAL)
    fsm.transition_to(IncidentState.REMEDIATING)
    fsm.transition_to(IncidentState.VERIFYING)
    fsm.transition_to(IncidentState.RESOLVED)
    assert fsm.current_state == IncidentState.RESOLVED


def test_fsm_critic_rejection_loops_back() -> None:
    fsm = IncidentStateMachine(initial_state=IncidentState.CRITIC_REVIEW)
    fsm.transition_to(IncidentState.INVESTIGATING)
    assert fsm.current_state == IncidentState.INVESTIGATING


def test_fsm_human_approval_rejection_aborts() -> None:
    fsm = IncidentStateMachine(initial_state=IncidentState.AWAITING_APPROVAL)
    fsm.transition_to(IncidentState.ABORTED)
    assert fsm.current_state == IncidentState.ABORTED


def test_fsm_illegal_transition_raises() -> None:
    fsm = IncidentStateMachine(initial_state=IncidentState.DETECTED)
    with pytest.raises(IllegalStateTransitionError) as exc_info:
        fsm.transition_to(IncidentState.REMEDIATING)
    assert "Illegal transition from DETECTED to REMEDIATING" in str(exc_info.value)
