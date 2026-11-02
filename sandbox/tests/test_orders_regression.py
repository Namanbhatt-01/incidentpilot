from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from sandbox.services.orders_api.app import app

client = TestClient(app)


def test_orders_api_health_endpoint() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_orders_api_successful_order_in_normal_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FAIL_MODE", "none")
    res = client.post(
        "/orders", json={"item_id": "item-123", "quantity": 2, "customer_id": "cust-abc"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CONFIRMED"
    assert data["order_id"].startswith("ord-")


def test_orders_api_500_regression_reproduced(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FAIL_MODE", "http500")
    res = client.post(
        "/orders", json={"item_id": "item-123", "quantity": 2, "customer_id": "cust-abc"}
    )
    assert res.status_code == 500
    assert "detail" in res.json()
    assert "NoneType" in res.json()["detail"] or "Internal Server Error" in res.json()["detail"]
