FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install debugpy for debugging
RUN pip install debugpy

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app/src

# Expose ports
EXPOSE 8000
EXPOSE 5678

# Run application with debugpy (with frozen modules disabled for proper debugging)
CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

