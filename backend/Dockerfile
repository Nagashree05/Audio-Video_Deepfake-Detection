FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git git-lfs && \
    rm -rf /var/lib/apt/lists/* && \
    git lfs install

# Set up working directory
WORKDIR /app

# Clone the repository with LFS files
RUN git clone --recursive https://github.com/Nagashree05/Audio-Video_Deepfake-Detection.git backend && \
    cd backend && \
    git lfs pull

WORKDIR /app/backend

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV TEMP_DIR=/app/temp_uploads

CMD ["python", "app/main.py"]
