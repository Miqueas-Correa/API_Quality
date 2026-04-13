import io
import pytest
import wave
import numpy as np
from PIL import Image

@pytest.fixture
def test_audio_bytes():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        samples = np.zeros(44100 * 1, dtype=np.int16)
        wav.writeframes(samples.tobytes())
    buffer.seek(0)
    return buffer.getvalue()

@pytest.fixture
def test_audio_file():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        samples = np.zeros(44100 * 1, dtype=np.int16)
        wav.writeframes(samples.tobytes())
    buffer.seek(0)
    return buffer

@pytest.fixture
def app():
    from src.app import create_app
    from src.config import TestingConfig
    return create_app(TestingConfig)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_image_file():
    img = Image.new('RGB', (100, 100), color='blue')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    buffer.seek(0)
    return buffer

@pytest.fixture
def test_image_bytes(test_image_file):
    return test_image_file.read()