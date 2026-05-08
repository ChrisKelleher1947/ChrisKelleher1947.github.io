# Deepfake Voice Detection System

Final Year Project Repository

[View Full Report](FYP-Semester-2-Report-20101947-ChrisKelleher.pdf)

---

## Project Overview

This project presents the design, training, and deployment of a deepfake voice detection system capable of identifying synthetic speech using deep learning.

The platform integrates:

- Deep learning audio classification
- WhatsApp chatbot integration
- FastAPI backend infrastructure
- AWS cloud deployment
- Real-time inference
- Audio preprocessing and augmentation

Users can submit audio through a web interface or WhatsApp bot and receive a prediction indicating whether the speech is:

- Bonafide (real human speech)
- Spoofed (AI-generated or synthetic speech)

---

## Project Poster

![Project Poster](ChrisKelleher-20101947-FYP-Poster.png)

---

# Live Demo

Test the deployed deepfake detection system below:

<p align="center">
  <a href="demo.html">
    <img src="https://img.shields.io/badge/Open-Live_Demo-blue?style=for-the-badge">
  </a>
</p>

### Important Notes

- Best performance is achieved using high-quality audio
- Heavy compression may reduce accuracy
- WhatsApp voice notes are significantly more difficult to classify due to Opus compression artefacts

---

# Documentation

## Core Project Pages

| Page | Description |
|---|---|
| [Project Architecture](ProjectArchitecture.md) | Full system architecture and cloud deployment |
| [Training Pipeline](TrainingPipeline.md) | Data preprocessing, augmentation, and training |
| [Wav2Vec2 Model](Wav2Vec2.md) | Transformer model implementation |
| [LSTM Model](LSTM.md) | Sequential spectrogram model |
| [CNN14 Model](CNN14.md) | PANNs CNN implementation |
| [Evaluation Results](Evaluation.md) | ROC-AUC, accuracy, and comparative evaluation |
| [WhatsApp Integration](WhatsAppBot.md) | WhatsApp bot implementation |
| [Deployment](Deployment.md) | AWS EC2 and SageMaker deployment |
| [Future Work](FutureWork.md) | Planned improvements and research |
| [Project Timeline](ProjectPlanTimeline.md) | Semester timeline and milestones |

---

# Deepfake Detection Flow

![Deepfake Detection Flow](FYP-Diagram.drawio.png)

The system operates as follows:

1. User submits an audio sample  
2. Audio is received by the backend  
3. Audio is preprocessed and normalised  
4. Data is forwarded to the deployed model  
5. The model returns confidence scores  
6. The system returns a prediction to the user  

---

# System Architecture

The final platform uses a distributed cloud architecture consisting of:

| Component | Purpose |
|---|---|
| WhatsApp Bot | User interaction and voice note collection |
| FastAPI Backend | Audio processing and API handling |
| AWS SageMaker | Machine learning model inference |
| AWS EC2 | Backend deployment and hosting |
| Web Interface | Browser-based testing environment |

This separation improves scalability, maintainability, and deployment flexibility.

---

# AI Training Pipeline

![AI Training Flow](aiTrainingFlow.png)

## Dataset

Primary dataset used:

- ASVspoof 2019 Logical Access Dataset

Additional data:

- Real WhatsApp voice notes
- Compression-affected mobile recordings

---

## Preprocessing Pipeline

The preprocessing stage includes:

- Audio resampling to 16kHz mono
- Silence trimming
- Amplitude normalisation
- Fixed-length segmentation
- Windowing
- Audio augmentation

---

## Augmentation Techniques

To improve robustness, the following augmentations were implemented:

- Opus codec simulation
- Noise injection
- Pitch shifting
- Volume scaling
- Frequency filtering

---

## Feature Extraction

| Model | Input Type |
|---|---|
| Wav2Vec2 | Raw waveform |
| LSTM | Log-Mel spectrogram |
| CNN14 | Mel-spectrogram |

---

# Model Selection

| Model | Architecture | Strategy |
|---|---|---|
| Wav2Vec2 | Transformer | Fine-tuned upper layers |
| CNN14 | CNN | Fine-tuned classification layers |
| LSTM | Sequential RNN | Spectrogram sequence learning |

---

# Evaluation Metrics

The following metrics were used during evaluation:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Equal Error Rate (EER)

ROC-AUC was treated as the primary evaluation metric due to its suitability for binary classification problems.

---

# Comparative Results

| Model | Performance Summary |
|---|---|
| Wav2Vec2 | Highest overall performance and strongest generalisation |
| CNN14 | Strong balance of efficiency and accuracy |
| LSTM | Good performance despite simpler architecture |

---

# Key Findings

## Strong Performance On

- High-quality recordings
- Podcasts
- Studio-quality speech
- AI-generated speech samples

## Performance Limitations

- WhatsApp compression
- Background noise
- Low-quality microphones
- Lossy audio transmission

The largest challenge identified was generalisation to heavily compressed real-world audio.

---

# Standardised Experimental Methodology

To ensure fair comparison between models:

- Identical preprocessing pipeline
- Identical dataset splits
- Identical training configuration
- Identical evaluation metrics

Only the model architecture itself was changed between experiments.

---

# Technologies Used

## Machine Learning

- PyTorch
- Hugging Face Transformers
- Torchaudio
- Scikit-learn

## Backend

- FastAPI
- Python
- FFmpeg

## Cloud Infrastructure

- AWS EC2
- AWS SageMaker
- Ngrok

## Messaging Integration

- WhatsApp-Web.js
- Node.js

---

# Repository Structure

```text
project/
│
├── README.md
├── demo.html
├── docs/
├── images/
├── backend/
├── frontend/
├── models/
├── training/
└── whatsapp-bot/
```

---

# Future Work

Potential future improvements include:

- Improved robustness to compression artefacts
- Larger real-world datasets
- Official WhatsApp Business API integration
- Real-time call analysis
- Explainable AI integration
- Domain adaptation techniques

---

# Author

Chris Kelleher

Final Year Project  
Deepfake Voice Detection via Deep Learning and WhatsApp Integration

---
