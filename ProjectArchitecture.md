## System Architecture

1. User forwards WhatsApp voice note
2. WhatsApp bot receives audio
3. Audio sent to FastAPI backend (EC2)
4. Backend sends audio to SageMaker endpoint
5. Model returns confidence score
6. Bot returns detection result to user

# The First Iteration

The first iteration of the project architecture did not account for the specifics of the machine learning segment of this project.
![Deepfake Detection Flow](FYP-Diagram.drawio.png)

The backend API system was not complete, and the processor section was kept simple, to allow for future development.
After the intital build of the project using the OpenAI whisper modle for transcribing audio, the ML platofrom used for the final iteration of the project was decided.
AWS SageMaker was chosen, due to its cloud integration with S3 and EC2 which the project moved towards in ints final development. A scalable solution for this project makes
the most sense when implemented with a cloud-based focus. SageMaker provider a suitable option for training and fine-tuning the models for this project in a way that synced well
with the rest of the project.

## Finalized Architecture Diagram

```mermaid
flowchart TD

    A["WhatsApp User \n Sends Voice Note"]

    subgraph AWS_Cloud_Environment
        B["EC2 Instance \n WhatsApp Bot (Baileys)"]
        C["FastAPI Backend \n Audio Processing"]
        D["SageMaker Endpoint \n Deepfake Detection Model"]
        E["Confidence Score (0–1)"]
        F["Amazon S3 \n Training Data & Model Artifacts"]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> C
    C --> B
    B --> A

    F -. Training Phase .-> D
```

## Training Diagram
```mermaid
flowchart LR

    A["Deepfake Audio Datasets\nASVspoof / VoxCeleb"]
    B["Preprocessing Pipeline\n16kHz Mono\nSilence Removal\nChunking"]
    C["Feature Extraction\nMel Spectrogram / Raw Audio"]
    D["Model Training\nCNN / LSTM / Wav2Vec2"]
    E["Evaluation Metrics\nAccuracy / F1 / ROC-AUC / EER"]
    F["Best Model Selection"]
    G["Model Artifact (.tar.gz)"]
    H["Amazon S3 Storage"]
    I["SageMaker Deployment"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
```
