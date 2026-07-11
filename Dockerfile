# ---- Stage 1: builder ----
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

# ---- Stage 2: runtime ----
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

WORKDIR /app

# Копируем виртуальное окружение
COPY --from=builder /build/.venv /app/.venv

# Копируем код
COPY src/ /app/src/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/

# Копируем entrypoint-скрипт
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Используем entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]