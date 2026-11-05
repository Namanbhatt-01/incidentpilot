# RB-001: Orders API 500 Internal Server Error & Discount Regression

## Overview
- **Service**: `orders-api`
- **Component**: Price rule & checkout validation
- **Severity**: P1 (Direct checkout failure)

## Symptoms & Alerts
- HTTP 500 Internal Server Error on `POST /orders`
- Error message in logs: `TypeError: 'NoneType' object is not subscriptable`
- Prometheus metric `http_requests_total{status="500"}` spiking above baseline

## Diagnosis
1. Inspect container logs for `FAIL_MODE=http500` or `TypeError` in discount calculation.
2. Verify if a recent deployment passed empty or uninitialized `price_rule` dictionary.
3. Check if regression reproduces on isolated curl/pytest test cases.

## Remediation Strategy
1. **Surgical Patch**:
   Add safe null-guard:
   ```python
   discount = price_rule["discount"] if price_rule else 0.0
   ```
2. **Rollback Action**:
   Revert container deployment to prior stable SHA or remove `FAIL_MODE=http500` environment variable:
   ```bash
   docker compose restart orders-api
   ```

## Verification
- Run regression test suite: `pytest sandbox/tests/test_orders_regression.py`
- Verify `POST /orders` returns HTTP 200 with confirmed `order_id`.

