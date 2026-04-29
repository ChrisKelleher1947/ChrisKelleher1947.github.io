"""
Diagnostic script to check if model labels are correct
and see what predictions look like on WhatsApp audio
"""

import os
import torch
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

MODEL_DIR = "./model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=== Loading Model ===")
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_DIR)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_DIR)
model = model.to(device)

if next(model.parameters()).dtype == torch.bfloat16:
    model = model.bfloat16()

model.eval()

# Check label mapping
print("\n=== Model Configuration ===")
print(f"id2label: {model.config.id2label}")
print(f"label2id: {model.config.label2id}")
print(f"Number of labels: {model.config.num_labels}")

print("\n⚠️  LABEL_0 and LABEL_1 are generic labels")
print("Based on training code:")
print("  LABEL_0 (index 0) = bonafide = REAL")
print("  LABEL_1 (index 1) = spoof = FAKE")

# Find a voice file to test
test_files = [f for f in os.listdir('.') if f.startswith('voice-') and f.endswith('.ogg')]

if test_files:
    test_file = test_files[0]
    print(f"\n=== Testing with: {test_file} ===")
    
    audio, _ = sf.read(test_file, dtype="float32")
    print(f"Loaded: {len(audio)} samples ({len(audio)/16000:.2f}s)")
    
    # Process exactly like training
    if len(audio) >= 64000:
        audio = audio[:64000]
    else:
        audio = np.pad(audio, (0, 64000 - len(audio)))
    
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak
    
    inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt", padding=False)
    input_values = inputs["input_values"].to(device)
    
    if next(model.parameters()).dtype == torch.bfloat16:
        input_values = input_values.bfloat16()
    
    with torch.no_grad():
        outputs = model(input_values=input_values)
        logits = outputs.logits[0].float().cpu().numpy()
        probs = torch.softmax(outputs.logits[0], dim=-1).float().cpu().numpy()
    
    print(f"\n=== Raw Model Output ===")
    print(f"Logits: {logits}")
    print(f"Probabilities: {probs}")
    
    print(f"\n=== Interpretation (0=REAL, 1=FAKE) ===")
    print(f"Real confidence: {probs[0]:.1%}")
    print(f"Fake confidence: {probs[1]:.1%}")
    
    verdict = "FAKE" if probs[1] >= 0.5 else "REAL"
    print(f"\nVerdict (threshold=0.5): {verdict}")
    
    print("\n" + "="*60)
    if probs[1] > 0.7:
        print("⚠️  HIGH FAKE SCORE on real WhatsApp audio!")
        print("This is a DOMAIN SHIFT issue:")
        print("  - Model was trained on clean studio audio")
        print("  - WhatsApp audio is heavily compressed")
        print("  - Model interprets compression as 'spoofing'")
        print("\nSOLUTION: Retrain with data augmentation that")
        print("simulates WhatsApp compression (see earlier advice)")
    elif probs[1] > 0.4:
        print("⚠️  Moderate fake score - borderline predictions")
        print("Consider adjusting threshold or retraining")
    else:
        print("✓ Model correctly identifies this as REAL")
    print("="*60)
    
else:
    print("\n⚠️  No voice-*.ogg files found")
    print("Send a voice message through WhatsApp bot first")