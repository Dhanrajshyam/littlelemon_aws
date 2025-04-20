# ---------- STAGE 1: Builder ----------

# Base image: Python 3.13 slim version for a minimal footprint
FROM python:3.13-slim AS builder

# Set working directory for all subsequent commands
WORKDIR /app

# Python environment variables:
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies:
# libpq-dev: Required for psycopg2 (PostgreSQL adapter)
# gcc: Required for compiling some Python packages
# Upgrade pip to latest version
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --upgrade pip

# Copy requirements file first to leverage Docker cache
COPY requirements.txt . 
# Install Python dependencies without storing pip cache
RUN pip install --user --no-cache-dir -r requirements.txt

# ---------- STAGE 2: Final image ----------

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
WORKDIR /app
    
# Add necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
    
# Copy only needed files
COPY . . 

# Document that the container listens on port 8000
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.prod.sh

# Set the entrypoint script as the default command
CMD ["/app/entrypoint.prod.sh"]
