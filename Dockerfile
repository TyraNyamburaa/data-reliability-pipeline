# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN groupadd --system pipeline && \
    useradd --system --gid pipeline --create-home pipeline

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data/raw ./data/raw
COPY data/processed ./data/processed
COPY data/quarantine ./data/quarantine
COPY tests ./tests

RUN chown -R pipeline:pipeline /app

USER pipeline

CMD ["python", "-m", "src.pipeline.main"]