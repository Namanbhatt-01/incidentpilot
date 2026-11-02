FROM python:3.11-slim

WORKDIR /app

COPY sandbox/services/orders_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sandbox/services/orders_api/ /app/sandbox/services/orders_api/

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "sandbox.services.orders_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
