import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # CORS Config
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False