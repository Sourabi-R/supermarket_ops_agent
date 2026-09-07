import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("DB_PATH", str(BASE_DIR / "data" / "supermarket.db"))).resolve()
DATASET_PATH = Path(os.getenv("DATASET_PATH", str(BASE_DIR / "data" / "raw" / "kirana_supermarket_demo_dataset.xlsx")).strip()).resolve()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
