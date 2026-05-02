import io
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

def quality_audio(file) -> bytes:
    extension = file.filename.rsplit(".", 1)[1].lower()
    audio = AudioSegment.from_file(file, format=extension)

    # 1. Estandarizar sample rate
    audio = audio.set_frame_rate(44100)

    # 2. Mantener stereo
    audio = audio.set_channels(2)

    # 3. Normalizar volumen
    audio = normalize(audio, headroom=0.5)

    # 4. Comprimir rango dinámico levemente
    audio = compress_dynamic_range(audio, threshold=-20.0, ratio=2.0, attack=5.0, release=50.0)

    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer.getvalue()