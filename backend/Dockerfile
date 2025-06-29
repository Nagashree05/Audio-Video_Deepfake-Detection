FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git git-lfs && \
    rm -rf /var/lib/apt/lists/* && \
    git lfs install

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app


# Clone the repository with LFS files
RUN git clone --recursive https://github.com/Nagashree05/Audio-Video_Deepfake-Detection.git backend && \
    cd backend && \
    git lfs pull


# Environment variables
ENV TEMP_DIR=/app/temp_uploads

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
