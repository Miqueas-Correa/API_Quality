import io
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from scipy.signal import butter, sosfilt

def butter_filter(samples, sr, filter_type, cutoff, order=4):
    sos = butter(order, cutoff, btype=filter_type, fs=sr, output='sos')
    return sosfilt(sos, samples)

def quality_audio(file) -> bytes:
    extension = file.filename.rsplit(".", 1)[1].lower()
    audio = AudioSegment.from_file(file, format=extension)

    # 1. Estandarizar sample rate
    audio = audio.set_frame_rate(44100)

    # 2. Mantener stereo (la música suena mejor en stereo)
    audio = audio.set_channels(2)

    # 3. Procesar cada canal por separado
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples = samples.reshape((-1, 2))  # separar canales L y R
    sr = audio.frame_rate

    enhanced = np.zeros_like(samples)
    for i in range(2):
        channel = samples[:, i]

        # Quitar frecuencias muy bajas (sub-bass sucio, < 30hz)
        channel = butter_filter(channel, sr, 'high', 30)

        # Realzar graves (80-200hz) — más cuerpo
        bass = butter_filter(channel, sr, 'band', [80, 200])
        channel = channel + bass * 0.3

        # Realzar presencia (2k-5khz) — más claridad en voces
        presence = butter_filter(channel, sr, 'band', [2000, 5000])
        channel = channel + presence * 0.2

        # Realzar aire (10k-16khz) — más brillo
        air = butter_filter(channel, sr, 'high', 10000)
        channel = channel + air * 0.15

        enhanced[:, i] = channel

    # 4. Normalizar para evitar clipping
    max_val = np.max(np.abs(enhanced))
    if max_val > 0:
        enhanced = enhanced / max_val * 32000

    # 5. Reconstruir audio
    audio = audio._spawn(enhanced.astype(np.int16).flatten().tobytes())

    # 6. Normalizar volumen
    audio = normalize(audio, headroom=0.5)

    # 7. Comprimir rango dinámico levemente
    audio = compress_dynamic_range(audio, threshold=-20.0, ratio=2.0, attack=5.0, release=50.0)

    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer.getvalue()