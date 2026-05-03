import io
from pydub import AudioSegment
from pydub.effects import normalize

def quality_audio(file) -> bytes:
    extension = file.filename.rsplit(".", 1)[1].lower()
    audio = AudioSegment.from_file(file, format=extension)

    # 1. Estandarizar sample rate
    audio = audio.set_frame_rate(44100)

    # 2. Mantener stereo
    audio = audio.set_channels(2)

    # 3. Normalizar volumen
    audio = normalize(audio, headroom=0.5)

    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer.getvalue()