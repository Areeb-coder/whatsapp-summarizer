from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

print("ENV PATH:", ENV_PATH)
print("KEY:", os.getenv("GEMINI_API_KEY"))
