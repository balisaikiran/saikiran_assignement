FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create data directory
RUN mkdir -p /app/data

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages with specific versions
RUN pip install --no-cache-dir numpy==1.21.0 && \
    pip install --no-cache-dir pandas==1.3.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the dataset
COPY ./data/test.csv /app/data/test.csv

# Copy application code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]