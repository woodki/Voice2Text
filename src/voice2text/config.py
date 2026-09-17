import os
import sys
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = (
    Path(sys.executable).resolve().parent
    if getattr(sys, 'frozen', False)
    else Path(__file__).resolve().parents[2]
)
load_dotenv(CONFIG_DIR / '.env')


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)