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

    A[WhatsApp User<br/>Sends Voice Note]

    subgraph AWS Cloud Environment
        B[EC2 Instance<br/>WhatsApp Bot (Baileys)]
        C[FastAPI Backend<br/>Audio Processing]
        D[Amazon SageMaker Endpoint<br/>Deepfake Detection Model]
        E[Confidence Score (0–1)]
        F[Amazon S3<br/>Training Data & Model Artifacts]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> C
    C --> B
    B --> A

    F --> D
```

## Training Diagram
## Model Training Architecture

```mermaid
flowchart LR

    A[Deepfake Audio Datasets<br/>ASVspoof / VoxCeleb]

    B[Preprocessing Pipeline<br/>16kHz Mono<br/>Silence Removal<br/>Chunking]

    C[Feature Extraction<br/>Mel Spectrogram / Raw Audio]

    D[Model Training<br/>CNN / LSTM / Wav2Vec2]

    E[Evaluation Metrics<br/>Accuracy<br/>F1 Score<br/>ROC-AUC<br/>EER]

    F[Best Model Selection]

    G[Model Artifact (.tar.gz)]

    H[Amazon S3 Storage]

    I[Amazon SageMaker Deployment]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
```
