# Use official slim Python 3.12 image
FROM python:3.12-slim

# Environment flags for container runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint separately first so script changes don't invalidate pip cache
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Copy application code last
COPY . /app/

# Ensure directory for persistent SQLite data
RUN mkdir -p /app/data /app/staticfiles

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]