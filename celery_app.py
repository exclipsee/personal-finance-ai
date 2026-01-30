"""Celery application configuration for background tasks."""
from __future__ import annotations

import os
from celery import Celery

BROKER = os.getenv("CELERY_BROKER_URL") or os.getenv("REDIS_URL") or os.getenv("REDIS_URL_LOCAL") or "redis://localhost:6379/0"
BACKEND = os.getenv("CELERY_RESULT_BACKEND") or BROKER

celery_app = Celery("personal_finance_ai", broker=BROKER, backend=BACKEND)

# Optional: configure some sane defaults
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
