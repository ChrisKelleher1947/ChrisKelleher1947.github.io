"""
main.py — FastAPI Deepfake Detection Backend
Receives audio from the WhatsApp bot, runs it through
the fine-tuned wav2vec2 model, returns a verdict.
"""
 
import os
import subprocess
import numpy as np
import soundfile as sf
import torch
from fastapi import FastAPI, UploadFile, File
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
 
# Settings
MODEL_DIR  = "./model"
SAMPLE_RATE = 16000
MAX_SAMPLES = 64000   # 4 seconds
FAKE_THRESHOLD = 0.5
 
# Load model once at startup
print("Loading model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_DIR)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_DIR)
 
model = model.to(device)
model.eval()
 
# Ensure dtype consistency
if device.type == "cuda" and next(model.parameters()).dtype == torch.bfloat16:
    print("Model is in bfloat16 - ensuring consistency")
    model = model.bfloat16()
 
print(f"Model loaded on {device}")
 
# Verify label mapping
print("\n=== Model Label Configuration ===")
print(f"id2label: {model.config.id2label}")
print(f"label2id: {model.config.label2id}")
 
# Expected from training: 0=bonafide (REAL), 1=spoof (FAKE)
LABELS_ARE_SWAPPED = False
if model.config.id2label == {0: 'LABEL_0', 1: 'LABEL_1'}:
    print("  WARNING: Generic labels detected - using training assumption (0=REAL, 1=FAKE)")
elif model.config.id2label.get(0) == 'spoof' or model.config.id2label.get(0) == 'LABEL_1':
    print("  WARNING: Labels appear to be swapped!")
    LABELS_ARE_SWAPPED = True
else:
    print(" Labels appear correct")
 
print("=" * 50 + "\n")
 
app = FastAPI()
 
 
# Health check
@app.get("/")
def health():
    return {"status": "running"}
 
 
# Detection endpoint
@app.post("/detect")
async def detect(file: UploadFile = File(...)):
 
    input_path  = "temp_input.ogg"
    output_path = "temp_converted.wav"
 
    try:
        # Save uploaded file
        with open(input_path, "wb") as f:
            f.write(await file.read())
 
        # Convert audio using ffmpeg
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-ar", str(SAMPLE_RATE),
            "-ac", "1",
            "-sample_fmt", "s16",
            output_path
        ], capture_output=True, text=True)
 
        if result.returncode != 0:
            print("FFmpeg error:", result.stderr)
            raise Exception("Audio conversion failed")
 
        # Load audio
        audio, _ = sf.read(output_path, dtype="float32")
        print(f"Audio loaded: {len(audio)} samples ({len(audio)/SAMPLE_RATE:.2f}s)")
 
        # Pad / truncate to 4 seconds
        if len(audio) >= MAX_SAMPLES:
            audio = audio[:MAX_SAMPLES]
        else:
            audio = np.pad(audio, (0, MAX_SAMPLES - len(audio)))
 
        # Normalize
        peak = np.abs(audio).max()
        if peak > 0:
            audio = audio / peak
 
        print(f"Audio normalized, peak: {peak:.4f}")
 
        # Feature extraction
        inputs = feature_extractor(
            audio,
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt",
            padding=False
        )
 
        input_values = inputs["input_values"].to(device)
 
        # Match model dtype if needed
        if next(model.parameters()).dtype == torch.bfloat16:
            input_values = input_values.bfloat16()
 
        # Inference
        with torch.no_grad():
            outputs = model(input_values=input_values)
 
            # Convert to float32 immediately
            logits = outputs.logits[0].float()
            probs = torch.softmax(logits, dim=-1)
 
        # Debug logs
        logits_np = logits.cpu().numpy()
        probs_np = probs.cpu().numpy()
        
        print(f"Raw logits: {logits_np}")
        print(f"Probabilities: [Real={probs_np[0]:.4f}, Fake={probs_np[1]:.4f}]")
 
        # Handle label swapping if detected
        if LABELS_ARE_SWAPPED:
            confidence_real = round(float(probs[1]), 3)
            confidence_fake = round(float(probs[0]), 3)
            print("(Labels swapped during extraction)")
        else:
            confidence_real = round(float(probs[0]), 3)
            confidence_fake = round(float(probs[1]), 3)
 
        verdict = "FAKE" if confidence_fake >= FAKE_THRESHOLD else "REAL"
 
        print(f"Verdict: {verdict} (Real={confidence_real}, Fake={confidence_fake}, threshold={FAKE_THRESHOLD})")
        print()
 
        return {
            "verdict": verdict,
            "confidence_real": confidence_real,
            "confidence_fake": confidence_fake,
        }
 
    finally:
        # Cleanup
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
 