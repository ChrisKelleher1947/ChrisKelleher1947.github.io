from fastapi import FastAPI, UploadFile, File
import whisper
import shutil

app = FastAPI()

# Load model once globally
model = whisper.load_model("small") 

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_path = "voice.ogg"
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe using Whisper
    result = model.transcribe(audio_path)
    return {"text": result["text"]}
