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
    
    # ANCHOR: Add your Auth0 configuration
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', '')
    AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE', '')
    AUTH0_ALGORITHMS = os.getenv('AUTH0_ALGORITHMS', 'RS256')
    AUTH0_ISSUER = f"https://{os.getenv('AUTH0_DOMAIN', '')}/" if os.getenv('AUTH0_DOMAIN') else ''