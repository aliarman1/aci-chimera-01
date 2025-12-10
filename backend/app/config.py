import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB default
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"]
    DATABASE_URL: str = "sqlite:///./chat_history.db"
    MAX_IMAGE_DIMENSION: int = 2048  # Resize images larger than this
    
settings = Settings()
