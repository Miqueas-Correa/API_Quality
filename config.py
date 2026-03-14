import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #  CORS configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    # Audio
    AUDIO_MAX_SIZE_MB = 20
    AUDIO_ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "aac", "m4a"}

    # Imágenes
    IMG_MAX_SIZE_MB = 20
    IMG_ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp", "tiff"}

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False