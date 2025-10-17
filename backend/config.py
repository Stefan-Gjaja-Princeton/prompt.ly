import os
from dotenv import load_dotenv

# Try to load from environment first, then fall back to api_key.py
load_dotenv()

try:
    from api_key import OPENAI_API_KEY as API_KEY_FROM_FILE
except ImportError:
    API_KEY_FROM_FILE = None

class Config:
    # Use environment variable first, then file, then None
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or API_KEY_FROM_FILE
    DATABASE_URL = 'sqlite:///promptly.db'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
