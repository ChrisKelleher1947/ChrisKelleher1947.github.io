## System Architecture

1. User forwards WhatsApp voice note
2. WhatsApp bot receives audio
3. Audio sent to FastAPI backend (EC2)
4. Backend sends audio to SageMaker endpoint
5. Model returns confidence score
6. Bot returns detection result to user

## Finalized Architecture Diagram
