from __future__ import annotations

from pathlib import Path

import yaml


def test_incident_pilot_template_schema_and_roles() -> None:
    template_path = Path("switch/templates/incident-pilot.template.yaml")
    assert template_path.exists(), "Template file must exist"

    data = yaml.safe_load(template_path.read_text())
    assert data.get("version") == 1
    assert "agents" in data
    assert "room" in data
    assert "kickoff" in data

    # Verify all 4 specialized agents are defined
    agent_names = [a["name"] for a in data["agents"]]
    assert "{team}-commander" in agent_names
    assert "{team}-diagnostician" in agent_names
    assert "{team}-debugger" in agent_names
    assert "{team}-critic" in agent_names

    # Verify room includes all 4 agents
    room_agents = data["room"]["agents"]
    assert len(room_agents) == 4

    # Verify agent providers and bridges
    providers = data["params"]["provider"]["default"]
    for expected_provider in ["claude", "codex", "opencode", "antigravity", "cursor"]:
        assert expected_provider in providers

    bridge_desc = data["params"]["bridge"]["description"].lower()
    for platform in ["slack", "teams", "discord", "telegram", "mattermost"]:
        assert platform in bridge_desc
