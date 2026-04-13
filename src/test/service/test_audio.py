import io
import wave
import pytest
from src.service.audio_service import quality_audio


class AudioFile:
    def __init__(self, buffer, filename):
        self._buffer = buffer
        self.filename = filename

    def read(self, size=-1):
        return self._buffer.read(size)

    def seek(self, pos, whence=0):
        return self._buffer.seek(pos, whence)

    def tell(self):
        return self._buffer.tell()


@pytest.fixture
def valid_audio_file(test_audio_file):
    test_audio_file.seek(0)
    return AudioFile(test_audio_file, "test.wav")


class TestQualityAudio:
    def test_quality_audio_returns_bytes(self, valid_audio_file):
        result = quality_audio(valid_audio_file)
        assert isinstance(result, bytes)

    def test_quality_audio_output_is_wav(self, valid_audio_file):
        result = quality_audio(valid_audio_file)
        buffer = io.BytesIO(result)
        with wave.open(buffer, 'rb') as wav:
            assert wav.getnchannels() > 0

    def test_quality_audio_sample_rate_44100(self, valid_audio_file):
        result = quality_audio(valid_audio_file)
        buffer = io.BytesIO(result)
        with wave.open(buffer, 'rb') as wav:
            assert wav.getframerate() == 44100

    def test_quality_audio_stereo_channels(self, valid_audio_file):
        result = quality_audio(valid_audio_file)
        buffer = io.BytesIO(result)
        with wave.open(buffer, 'rb') as wav:
            assert wav.getnchannels() == 2