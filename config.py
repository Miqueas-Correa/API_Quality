import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # CORS Config
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
    
    # config.py
class Config:
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    # Audio
    AUDIO_MAX_SIZE_MB = 50
    AUDIO_ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "aac", "m4a"}

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False