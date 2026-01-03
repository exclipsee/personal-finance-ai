FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies only in the builder stage
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       g++ \
       git \
       curl \
       libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and build wheel cache
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only runtime OS deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy built wheels from builder and install them, then remove wheels to keep image small
COPY --from=builder /wheels /wheels
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# Copy project
COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
