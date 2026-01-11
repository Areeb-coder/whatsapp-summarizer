import os
from pathlib import Path
from dotenv import load_dotenv

# 🔴 FORCE LOAD .env USING ABSOLUTE PATH (WINDOWS SAFE)
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Optional debug (remove later if you want)
print("GEMINI_API_KEY loaded:", os.getenv("GEMINI_API_KEY") is not None)

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from summarizer import summarize_chat
from whatsapp_zip_adapter import parse_whatsapp_zip


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    """
    Accepts a WhatsApp .txt file OR a .zip containing a WhatsApp export.
    Adapter normalizes the data.
    Summarizer remains unchanged.
    """

    # Save uploaded file temporarily
    temp_path = BASE_DIR / f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Adapter layer (handles txt or zip internally)
    messages = parse_whatsapp_zip(str(temp_path))

    # Existing summariser logic (UNCHANGED)
    summary = summarize_chat(messages)

    # Cleanup
    try:
        os.remove(temp_path)
    except Exception:
        pass

    return {"summary": summary}
