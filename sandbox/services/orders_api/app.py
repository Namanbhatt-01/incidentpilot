from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="orders-api", version="1.0.0")


class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    customer_id: str


@app.get("/health")
def health() -> dict[str, str]:
    fail_mode = os.getenv("FAIL_MODE", "none")
    return {"status": "ok", "fail_mode": fail_mode}


@app.post("/orders")
def create_order(req: OrderRequest) -> dict[str, Any]:
    fail_mode = os.getenv("FAIL_MODE", "none")

    # Injected Chaos Failure: http500
    if fail_mode == "http500":
        # Simulates regression in discount rule engine where price_rule is None
        price_rule: dict[str, float] | None = None
        try:
            # Bug: Accessing NoneType subscript raises TypeError -> 500
            price_rule["discount"]  # type: ignore[index]
        except TypeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"TypeError: 'NoneType' object is not subscriptable in price calculation: {e}",
            ) from e

    unit_price = 29.99
    total = unit_price * req.quantity
    order_id = f"ord-{uuid.uuid4().hex[:6]}"

    return {
        "order_id": order_id,
        "status": "CONFIRMED",
        "item_id": req.item_id,
        "quantity": req.quantity,
        "total": total,
    }
