# Audio-Video Deepfake Detection

# Overview
Audio-Video Deepfake Detection is a full-stack AI application that leverages deep learning models to detect deepfakes in both audio and video files. The project features a modern web interface and robust backend, allowing users to upload media and receive deepfake detection results in real time.

# Features

	🎥 Video deepfake detection using ResNet50
	🎤 Audio deepfake detection using VGG16+LSTM
	🌐 Web frontend (React or Streamlit)
	📊 Confidence scores and result dashboard
	🗂️ Detection history (optional)
	🔒 User authentication (optional)
	🚀 Easy deployment (Docker, Railway, Render)
	☁️ Model weights hosted on Hugging Face Hub for easy access and portability

# Model Information

	Video Model: ResNet50 trained for deepfake detection.
	Audio Model: VGG16 + LSTM trained for audio deepfake detection.
	Model Hosting: All models are stored and loaded from Hugging Face Hub for reliability and portability.
	Custom Loss: Focal Loss for imbalanced data.

Model Storage
All trained model weights are hosted on the Hugging Face Hub for reliable, versioned, and fast downloads.
	Repository: https://huggingface.co/nagashreens05/deepguard/tree/main1

How Models Are Loaded
The backend code references these models directly from Hugging Face using the Keras-Hugging Face integration:

python
import keras
model = keras.saving.load_model("model_link")
This requires the huggingface_hub and a recent version of keras (pip install -U keras huggingface_hub).

No need to manually download or store large model files in your repository or Docker image.
See the Hugging Face documentation for more details.

# Setup & Installation

# Backend (FastAPI)

Clone the repository:
git clone https://github.com/Nagashree05/Audio-Video_Deepfake-Detection.git
cd Audio-Video_Deepfake-Detection/backend

Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install dependencies:
pip install --upgrade pip
pip install -r requirements.txt

Run the backend server:
uvicorn app.main:app --reload

# Frontend (React)

Navigate to the frontend directory:
cd ../frontend

Install frontend dependencies:
npm install

Start the frontend development server:
npm run dev

# Usage

Open the frontend in your browser (http://localhost:3000).
Upload a video or audio file.
View the detection result and confidence score.

# Deployment

Docker
	Build the Docker image:
	docker build -t deepfake-backend ./backend
	Run the container:
	docker run -p 8000:8000 deepfake-backend

Railway/Render
	Set the root directory to backend.
	Use the Dockerfile provided.
	Set the start command to:
	uvicorn app.main:app --host 0.0.0.0 --port $PORT

Models will be automatically downloaded from Hugging Face at runtime.

Troubleshooting
ModuleNotFoundError: Ensure your working directory and import paths are correct.
Model file not found: Check Hugging Face model path and your internet connection.
CORS errors: Make sure CORS is enabled in your FastAPI backend.
TensorFlow warnings: These are informational; for CPU-only environments, they can be ignored.

License
This project is licensed under the MIT License.
