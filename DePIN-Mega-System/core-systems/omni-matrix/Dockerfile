# Omni-Matrix Docker Image
# Zero-Cost Decentralized Cloud Platform

FROM python:3.11-slim

LABEL maintainer="Omni-Matrix Team <dev@omni-matrix.io>"
LABEL description="Zero-Cost Decentralized Cloud Computing Platform"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs data cache

# Expose ports
# 8080 - HTTP API
# 9090 - Prometheus metrics
# 5001 - IPFS API
# 4001 - IPFS Swarm
EXPOSE 8080 9090 5001 4001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run command
CMD ["python", "main.py"]
