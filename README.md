# Deepfake Voice Detection System

Final Year Project — Deepfake Voice Detection Using Deep Learning with Real-Time WhatsApp Integration

---

## Project Overview

This project presents the design, training, evaluation, and deployment of an AI-driven deepfake voice detection system capable of identifying synthetic speech from real human speech.

The system combines:

- Deep learning audio classification
- Cloud-hosted inference
- A WhatsApp chatbot interface
- A browser testing platform
- Real-time backend processing

The primary objective was to investigate whether modern speech models could be integrated into widely used communication platforms to provide accessible deepfake voice detection for real-world users.

---

## System Poster

![Project Poster](ChrisKelleher-20101947-FYP-Poster.png)

---

# Repository

GitHub Pages Repository:

https://github.com/ChrisKelleher1947/ChrisKelleher1947.github.io

---

## Live Demonstration

The deployed web interface allows users to upload audio files and receive a prediction indicating whether the audio is likely genuine or synthetic.

### Open the Live Demo

<a href="demo.html">
    <button>Launch Demo</button>
</a>

### Recommended Audio

Best performance is achieved with:

- High-quality microphone recordings
- Minimal background noise
- WAV or high bitrate audio

Performance may degrade with:

- WhatsApp voice notes
- Heavy compression
- Low bitrate recordings
- Excessive background noise

---

# Project Sections

---

## 1. Dataset Exploration

The project began with a full exploration of the ASVspoof 2019 Logical Access dataset.

### Topics Covered

- Dataset structure
- Label analysis
- Waveform visualisation
- Log-Mel spectrogram analysis
- Class imbalance inspection

### Included Analysis

- Real vs fake waveform comparison
- Spectrogram comparisons
- Audio distribution analysis
- Frequency-domain inspection

---

## 2. Wav2Vec2 Training Pipeline

The primary model used in this project was a fine-tuned Wav2Vec2 transformer architecture.

### Pipeline Components

- GPU configuration
- Dataset loading
- Multi-source integration
- Audio preprocessing
- Augmentation pipeline
- Feature extraction
- Fine-tuning strategy
- Weighted sampling
- Optimisation setup
- Training loop implementation

### Key Features

- Raw waveform learning
- Transfer learning
- Mixed precision training
- Opus codec simulation
- FFmpeg preprocessing
- Early stopping
- ROC-AUC evaluation

---

## 3. LSTM Model Development

A bidirectional LSTM architecture was implemented as a secondary comparison model.

### Features

- Mel-spectrogram inputs
- Sequential modelling
- Bidirectional processing
- Spectrogram preprocessing
- Recurrent neural network classification

### Included Topics

- Spectrogram generation
- Dataset adaptation
- LSTM architecture design
- Training configuration
- Evaluation pipeline

---

## 4. CNN14 PANNs Model

The CNN14 architecture from the PANNs framework was implemented as a convolutional baseline model.

### Features

- Time-frequency feature extraction
- Mel-spectrogram input representation
- CNN feature learning
- Efficient training pipeline

### Included Topics

- Spectrogram preprocessing
- CNN input formatting
- Forward pass implementation
- Loss calculation
- Evaluation pipeline

---

## 5. Model Evaluation

All models were evaluated using identical preprocessing pipelines and evaluation metrics to ensure fair comparison.

### Evaluation Metrics

- Loss
- Accuracy
- ROC-AUC
- Classification performance
- Training convergence

### Models Evaluated

| Model | Input Type | Performance |
|---|---|---|
| Wav2Vec2 | Raw waveform | Highest overall |
| CNN14 | Spectrogram | Strong balance |
| LSTM | Spectrogram | Competitive baseline |

### Included Graphs

- Loss curves
- Accuracy curves
- ROC-AUC curves
- Comparative model analysis

---

## 6. System Evaluation

The complete end-to-end system was evaluated under real-world conditions.

### Components Evaluated

- WhatsApp chatbot
- Web upload system
- FastAPI backend
- AWS deployment
- Audio preprocessing pipeline

### Key Findings

- Strong performance on high-quality audio
- Significant degradation on compressed WhatsApp audio
- Compression artefacts heavily affect classification accuracy
- Windowing improves robustness on long-form audio

---

## 7. Cloud System Architecture

The deployed system uses a distributed cloud architecture.

## Architecture Components

| Component | Purpose |
|---|---|
| WhatsApp Bot | User interaction |
| FastAPI Backend | Audio processing |
| AWS EC2 | Backend hosting and Model Inference |
| FFmpeg | Audio conversion |

---

## System Architecture Diagram

![Architecture Diagram](Project_Diagram.png)

---

## 8. Training Pipeline

The AI training workflow follows a structured deep learning pipeline.

![Training Pipeline](aiTrainingFlow.png)

### Pipeline Stages

1. Dataset loading
2. Audio preprocessing
3. Data augmentation
4. Feature extraction
5. Model training
6. Validation and evaluation
7. Model selection
8. Deployment

---

## 9. Real-World Challenges

The project identified several major deployment challenges.

### Primary Limitation

WhatsApp voice compression introduces severe audio degradation through the Opus codec.

### Effects on Performance

- Loss of high-frequency speech information
- Reduced waveform fidelity
- Increased false positives
- Lower generalisation performance

### Additional Challenges

- Environmental noise
- Low-quality microphones
- Packet loss
- Variable bitrate encoding

---

## 10. Future Improvements

Several future improvements were identified during evaluation.

### Possible Enhancements

- Increased real-world training data
- More aggressive codec simulation
- Domain adaptation techniques
- Adversarial training
- Official WhatsApp Business API integration
- Real-time call analysis
- Improved explainability tools

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| PyTorch | Deep learning framework |
| Hugging Face Transformers | Wav2Vec2 implementation |
| Torchaudio | Audio processing |
| FFmpeg | Audio conversion |
| FastAPI | Backend API |
| AWS EC2 | Hosting |
| AWS SageMaker | Model deployment |
| Node.js | WhatsApp integration |
| WhatsApp-Web.js | Chatbot interface |

---

# Experimental Methodology

To ensure scientifically valid comparison between models:

- Identical datasets
- Identical train/validation splits
- Identical preprocessing
- Identical augmentation strategy
- Identical evaluation metrics

The only changing variable between experiments was the model architecture.

---

# Key Findings

| Finding | Outcome |
|---|---|
| Wav2Vec2 performance | Best overall |
| CNN14 performance | Strong balance of speed and accuracy |
| LSTM performance | Competitive despite simplicity |
| Spectrogram models | Effective but less robust |
| Compression handling | Major weakness |
| Real-world deployment | Challenging due to audio degradation |

---

# Conclusion

This project successfully demonstrates the feasibility of integrating deep learning-based synthetic speech detection into real-world communication systems.

The implemented platform combines:

- Deep learning audio classification
- Cloud-hosted inference
- Messaging platform integration
- Real-time processing

While strong performance was achieved on high-quality audio, the project also highlights the difficulty of detecting synthetic speech in heavily compressed real-world environments.

The system provides a strong foundation for future research into practical and scalable deepfake voice detection technologies.

---
