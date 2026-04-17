import os
import uuid
import subprocess
import numpy as np
import soundfile as sf
import torch

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

# Config
MODEL_DIR = "./model"
SAMPLE_RATE = 16000
MAX_SAMPLES = 64000   # 4 seconds
FAKE_THRESHOLD = 0.5

# App Setup
app = FastAPI()

# Allow GitHub Pages and ngrok frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
print("Loading model...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_DIR)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_DIR)

model = model.to(device)
model.eval()

if device.type == "cuda" and next(model.parameters()).dtype == torch.bfloat16:
    model = model.bfloat16()

print(f"Model loaded on {device}")

print("Label config:")
print(model.config.id2label)

LABELS_ARE_SWAPPED = False

if model.config.id2label == {0: "LABEL_0", 1: "LABEL_1"}:
    print("Warning: generic labels detected")
elif "spoof" in str(model.config.id2label.get(0, "")):
    LABELS_ARE_SWAPPED = True

print("System ready\n")

# Health Check
@app.get("/")
def health():
    return {
        "status": "running",
        "model": "wav2vec2-deepfake-detector"
    }

# Main Route
@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    job_id = str(uuid.uuid4())

    input_path = f"temp_input_{job_id}.ogg"
    output_path = f"temp_output_{job_id}.wav"

    try:
        # Save upload
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Convert audio
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

        # Load audio
        audio, _ = sf.read(output_path, dtype="float32")

        print(f"Audio: {len(audio)} samples")

        # Trim / pad
        if len(audio) >= MAX_SAMPLES:
            audio = audio[:MAX_SAMPLES]
        else:
            audio = np.pad(audio, (0, MAX_SAMPLES - len(audio)))

        # Normalize
        peak = np.abs(audio).max()
        if peak > 0:
            audio = audio / peak

        # Feature extraction
        inputs = feature_extractor(
            audio,
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt",
            padding=False
        )

        input_values = inputs["input_values"].to(device)

        if next(model.parameters()).dtype == torch.bfloat16:
            input_values = input_values.bfloat16()

        # Inference
        with torch.no_grad():
            outputs = model(input_values=input_values)
            logits = outputs.logits[0].float()
            probs = torch.softmax(logits, dim=-1)

        probs = probs.cpu().numpy()

        # Handle labels
        if LABELS_ARE_SWAPPED:
            confidence_real = float(probs[1])
            confidence_fake = float(probs[0])
        else:
            confidence_real = float(probs[0])
            confidence_fake = float(probs[1])

        verdict = "FAKE" if confidence_fake >= FAKE_THRESHOLD else "REAL"

        print(f"Verdict: {verdict}")

        return {
            "verdict": verdict,
            "confidence_real": round(confidence_real, 3),
            "confidence_fake": round(confidence_fake, 3)
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
        # cleanup safely
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass