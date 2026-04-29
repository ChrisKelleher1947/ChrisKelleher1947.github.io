import os
import uuid
import subprocess
import numpy as np
import soundfile as sf
import torch

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

# Configuration values for model and audio preprocessing
MODEL_DIR = "./model"
SAMPLE_RATE = 16000

WINDOW_SIZE = 64000
STRIDE = 32000

FAKE_THRESHOLD = 0.5

# Initialize FastAPI application and configure CORS for external access
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and feature extractor, and assign execution device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_DIR)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_DIR)

model = model.to(device)
model.eval()

# Enable bfloat16 precision if supported for faster computation
if device.type == "cuda" and next(model.parameters()).dtype == torch.bfloat16:
    model = model.bfloat16()

# Detect whether model label mapping is potentially inverted
LABELS_ARE_SWAPPED = False

if model.config.id2label == {0: "LABEL_0", 1: "LABEL_1"}:
    print("Warning: Generic labels detected")
elif "spoof" in str(model.config.id2label.get(0, "")):
    LABELS_ARE_SWAPPED = True

# Health check endpoint to confirm API is running
@app.get("/")
def health():
    return {
        "status": "running",
        "model": "wav2vec2-deepfake-multiframe"
    }

# Splits audio into overlapping windows to improve prediction stability
def create_windows(audio, window_size, stride):
    if len(audio) <= window_size:
        return [np.pad(audio, (0, window_size - len(audio)))]

    windows = []

    for start in range(0, len(audio) - window_size + 1, stride):
        windows.append(audio[start:start + window_size])

    last_start = len(audio) - window_size
    if windows[-1].shape[0] != window_size:
        windows.append(audio[last_start:last_start + window_size])

    return windows

# Main inference endpoint that processes uploaded audio and returns classification
@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    job_id = str(uuid.uuid4())

    input_path = f"temp_input_{job_id}.ogg"
    output_path = f"temp_output_{job_id}.wav"

    try:
        # Save uploaded file to temporary storage
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Convert audio into compatible wav format using ffmpeg
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-ar", str(SAMPLE_RATE),
            "-ac", "1",
            "-sample_fmt", "s16",
            output_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return {
                "verdict": "ERROR",
                "error": "FFmpeg conversion failed",
                "confidence_real": 0.0,
                "confidence_fake": 0.0
            }

        # Load converted audio file into memory
        audio, _ = sf.read(output_path, dtype="float32")

        # Segment audio into overlapping windows for inference
        windows = create_windows(audio, WINDOW_SIZE, STRIDE)

        print(f"Processing {len(windows)} windows")

        all_probs = []

        # Run model inference on each audio window
        for window in windows:

            peak = np.abs(window).max()
            if peak > 0:
                window = window / peak

            inputs = feature_extractor(
                window,
                sampling_rate=SAMPLE_RATE,
                return_tensors="pt",
                padding=False
            )

            input_values = inputs["input_values"].to(device)

            if next(model.parameters()).dtype == torch.bfloat16:
                input_values = input_values.bfloat16()

            with torch.no_grad():
                outputs = model(input_values=input_values)
                logits = outputs.logits[0].float()
                probs = torch.softmax(logits, dim=-1)

            all_probs.append(probs.cpu().numpy())

        # Aggregate predictions across all windows
        all_probs = np.array(all_probs)
        avg_probs = np.mean(all_probs, axis=0)

        # Map probabilities depending on label configuration
        if LABELS_ARE_SWAPPED:
            confidence_real = float(avg_probs[1])
            confidence_fake = float(avg_probs[0])
        else:
            confidence_real = float(avg_probs[0])
            confidence_fake = float(avg_probs[1])

        verdict = "FAKE" if confidence_fake >= FAKE_THRESHOLD else "REAL"

        print(f"Verdict: {verdict}")

        return {
            "verdict": verdict,
            "confidence_real": round(confidence_real, 3),
            "confidence_fake": round(confidence_fake, 3),
            "windows_processed": len(windows)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "verdict": "ERROR",
            "error": str(e),
            "confidence_real": 0.0,
            "confidence_fake": 0.0
        }

    finally:
        # Cleanup temporary files created during processing
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass