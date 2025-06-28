FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app/backend

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV TEMP_DIR=/app/temp_uploads

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]