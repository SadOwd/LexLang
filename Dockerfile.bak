# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_CACHE_DIR=/root/.cache/pip

WORKDIR /app

# --- Builder stage ---
FROM base AS builder

# Install build dependencies
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first for better cache usage
COPY --link pyproject.toml ./
COPY --link setup.cfg ./
COPY --link setup.py ./
COPY --link requirements.txt ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    if [ -f requirements.txt ]; then .venv/bin/pip install -r requirements.txt; fi && \
    if [ -f pyproject.toml ]; then .venv/bin/pip install .; fi

# --- Final stage ---
FROM base AS final

# Create non-root user
RUN addgroup --system lexlang && adduser --system --ingroup lexlang lexlang
USER lexlang

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code and relevant directories (excluding secrets, git, etc.)
COPY --link src/ ./src/
COPY --link configs/ ./configs/
COPY --link models/ ./models/
COPY --link data/ ./data/
COPY --link Makefile ./
COPY --link README.md ./

# Expose the default port
EXPOSE 8000

# Healthcheck (optional, can be customized)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# Default command to run the FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
