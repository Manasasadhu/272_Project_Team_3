FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including git for cloning)
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the latest code from main branch
RUN git clone --branch main https://github.com/Manasasadhu/272_Project_Team_3.git /tmp/repo && \
    cp -r /tmp/repo/agentic/* /app/ && \
    rm -rf /tmp/repo

# Copy requirements (already cloned above, but keeping for clarity)
# Already in /app from git clone

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install debugpy for debugging
RUN pip install debugpy

# Set Python path
ENV PYTHONPATH=/app/src

# Expose ports
EXPOSE 8000
EXPOSE 5678

# Run application with debugpy (with frozen modules disabled for proper debugging)
CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

