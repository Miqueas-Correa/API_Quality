import io
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter

def quality_image(file, extension: str) -> bytes:
    # Leer imagen
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 1. Reducir ruido preservando bordes
    img = cv2.fastNlMeansDenoisingColored(img, None, h=6, hColor=6, templateWindowSize=7, searchWindowSize=21)

    # 2. Upscaling x2 con interpolación de alta calidad
    height, width = img.shape[:2]
    img = cv2.resize(img, (width * 2, height * 2), interpolation=cv2.INTER_LANCZOS4)

    # 3. Sharpening (nitidez)
    kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ])
    img = cv2.filter2D(img, -1, kernel)

    # Convertir a PIL para ajustes de color
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # 4. Mejorar brillo levemente
    img_pil = ImageEnhance.Brightness(img_pil).enhance(1.05)

    # 5. Mejorar contraste
    img_pil = ImageEnhance.Contrast(img_pil).enhance(1.15)

    # 6. Mejorar saturación de colores
    img_pil = ImageEnhance.Color(img_pil).enhance(1.2)

    # 7. Nitidez final con PIL
    img_pil = img_pil.filter(ImageFilter.SHARPEN)

    # Exportar
    buffer = io.BytesIO()
    fmt = "JPEG" if extension in ("jpg", "jpeg", "jfif") else extension.upper()
    img_pil.save(buffer, format=fmt, quality=95)
    buffer.seek(0)
    return buffer.getvalue()