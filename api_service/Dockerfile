FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r appuser && useradd -r -g appuser app  && chown -R  app:appuser /app/* && chown -R app:appuser /app && chmod 700 /app

ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://collector-service.default.svc.cluster.local:4317

EXPOSE 8000

USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]
