# ======== Stage 1: Builder ========
FROM python:3.12-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# ======== Stage 2: Final Image ========
FROM python:3.12-slim

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set PATH to include venv
ENV PATH="/opt/venv/bin:$PATH"

# Set app directory
WORKDIR /app

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run database migrations at startup (optional)
# If you don’t use Alembic, remove this line

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
