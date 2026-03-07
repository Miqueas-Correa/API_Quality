import io
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

def quality_audio(file) -> bytes:
    # Leer el archivo
    extension = file.filename.rsplit(".", 1)[1].lower()
    audio = AudioSegment.from_file(file, format=extension)

    # 1. Convertir a mono (mejora el procesamiento)
    audio = audio.set_channels(1)

    # 2. Estandarizar sample rate a 44100hz
    audio = audio.set_frame_rate(44100)

    # 3. Eliminar ruido de fondo
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    reduced = nr.reduce_noise(y=samples, sr=audio.frame_rate, stationary=False)

    # 4. Reconstruir AudioSegment desde el array limpio
    audio = audio._spawn(reduced.astype(np.int16).tobytes())

    # 5. Normalizar volumen (-3db para evitar clipping)
    audio = normalize(audio, headroom=3.0)

    # 6. Comprimir rango dinámico (balancea partes muy fuertes/débiles)
    audio = compress_dynamic_range(audio)

    # 7. Exportar como bytes
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer.getvalue()