# FYP Pages  
Final Year Project GitHub Pages Repository
Project Repo: https://github.com/ChrisKelleher1947/ChrisKelleher1947.github.io
[Final Report/Documentaion](FYP-Semester-2-Report-20101947-ChrisKelleher.pdf)

---

## Project Overview

This project presents the design, training, and deployment of an AI deepfake voice detection system. The system is capable of analysing audio input and returning a confidence score indicating whether the audio is genuine or synthetic.

A cloud architecture is used to support scalability, integrating a WhatsApp bot, a FastAPI backend, and a machine learning model hosted on AWS SageMaker.

![Project Poster](ChrisKelleher-20101947-FYP-Poster.png)


---

## Live Demo

Interact with the deepfake detection model below:

<a href="demo.html">
    <button>Open Live Demo</button>
</a>

*Note: Best results are achieved with high-quality audio. Heavily compressed audio may reduce detection accuracy.*

---

## Page Directory

- [Project Architecture](ProjectArchitecture.md)  
- [Project Timeline Semester 2](ProjectPlanTimeline.md)

---

## Model Selection

| Model       | Pretrained Base             | Fine-tuning Strategy                                      |
|-------------|-----------------------------|-----------------------------------------------------------|
| Transformer | `Gustking/wav2vec2`         | Fine-tune upper layers + classification head              |
| CNN         | `PANNs cnn14`               | Replace dense output and fine-tune final convolutional layers |
| LSTM        | `OpenL3 embeddings → LSTM`  | Train LSTM layers with a final dense classification layer |

---

## Deepfake Detection Flow

![Deepfake Detection Flow](FYP-Diagram.drawio.png)

The system operates as follows:

1. A user submits an audio sample via WhatsApp or the web interface  
2. The audio is received by the backend system  
3. The FastAPI backend processes and formats the audio  
4. The processed audio is sent to the deployed model  
5. The model returns confidence scores for “real” and “fake” classifications  
6. The result is returned to the user  

---

## System Architecture

The final system is built using a cloud architecture:

- **WhatsApp Bot (Node.js / WhatsApp-web)** for user interaction  
- **FastAPI Backend** for audio processing and API handling  
- **Amazon SageMaker** for model deployment  
- **Amazon EC2** for server deployment  

This architecture enables scalability and separation of concerns across system components.

---

## Training Pipeline

![AI Training Flow](aiTrainingFlow.png)

The training process follows a structured pipeline:

1. **Datasets**  
   - ASVspoof    

2. **Preprocessing**  
   - Audio resampled to 16kHz mono  
   - Silence trimming  
   - Normalisation  
   - Fixed length segmentation  

3. **Feature Extraction**  
   - Log-Mel Spectrograms  
   - Raw waveform input (for transformer models)  

4. **Model Training**  
   - CNN, LSTM, and Transformer architectures evaluated  

5. **Evaluation Metrics**  
   - Accuracy  
   - Precision / Recall  
   - F1 Score  
   - ROC-AUC  
   - Equal Error Rate (EER)  

6. **Model Selection**  
   - Best performing model selected based on performance and stability  

7. **Deployment**  
   - Model packaged and deployed via SageMaker endpoint  

---

## Standardised Experimental Methodology

To ensure fair and scientifically valid comparisons between models:

- Identical preprocessing pipeline  
- Identical dataset splits  
- Identical training configuration  
- Identical evaluation metrics  
- Only variable changed: **model architecture**

This ensures that performance differences are attributable solely to the model design.

---

## Final System Workflow

1. User submits an audio sample  
2. Audio is received by the backend  
3. Audio is preprocessed and normalised  
4. Data is sent to the deployed model  
5. Model returns confidence scores  
6. System returns a classification result to the user  

---

## Limitations

- Heavily compressed audio (e.g. WhatsApp voice notes) significantly reduces detection accuracy  
- The model performs best on higher quality audio inputs  
- Further research is required for robust detection on low bitrate, lossy audio formats  

---

## References

Tech With Tim (2025) *How To Build an API with Python (LLM Integration, FastAPI, Ollama & More)* [YouTube video]. Available at: https://www.youtube.com/watch?v=cy6EAp4iNN4  
(Accessed: 2 December 2025)

Meta (n.d.) *WhatsApp Cloud API Documentation*. Available at: https://developers.facebook.com/docs/whatsapp/cloud-api  
(Accessed: 2 December 2025)

Solanki, R. et al. (n.d.) *Artificial Intelligence to Combat Audio Fraud: A Flask-Deployed Hybrid Deep Learning System*. IEEE. Available at: https://ieeexplore.ieee.org/document/10778737  
(Accessed: 2 December 2025)

Stryker, C. (n.d.) *What is a recurrent neural network?* IBM. Available at: https://www.ibm.com/think/topics/recurrent-neural-networks  
(Accessed: 2 December 2025)

Jayakannan, S. M. (2025) *Securing Voice-Based Financial Authentication in the Era of AI Voice Cloning*, Journal of Computer Science and Technology Studies, 7(4), pp. 515–520.  

Stafford, G.A. (2025) *Fine-Tuning Wav2Vec2 for Real-Time Deepfake Audio Detection*, Data Science Collective. Available at: https://medium.com/data-science-collective/fine-tuning-wav2vec2-for-real-time-deepfake-audio-detection-b72d7efebdd7
