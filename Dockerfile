# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN groupadd --system pipeline && \
    useradd --system --gid pipeline --create-home pipeline

COPY requirements/base.txt ./requirements/base.txt

RUN pip install --no-cache-dir -r requirements/base.txt

COPY src ./src
COPY data/raw ./data/raw
COPY config ./config

RUN mkdir -p /app/data/processed /app/data/quarantine /app/data/reports && \
    chown -R pipeline:pipeline /app

USER pipeline

CMD ["python", "-m", "src.pipeline.main"]
