import io
from unittest.mock import patch


# ✅ Sin archivo
def test_post_image_no_file(client):
    response = client.post("/img")
    assert response.status_code == 400
    assert response.json["error"] == "No se proporcionó ningún archivo"


# ✅ Archivo vacío
def test_post_image_empty_filename(client):
    data = {"file": (io.BytesIO(b""), "")}
    response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.json["error"] == "El archivo está vacío"


# ✅ Formato no permitido
def test_post_image_invalid_format(client):
    data = {"file": (io.BytesIO(b"fake content"), "image.txt")}
    response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 415
    assert response.json["error"] == "Formato no permitido"


# ✅ Archivo muy grande
def test_post_image_too_large(client, test_image_bytes):
    data = {"file": (io.BytesIO(test_image_bytes), "image.png")}
    with patch.dict(client.application.config, {"IMG_MAX_SIZE_MB": 0.00001}):
        response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 413


# ✅ Imagen válida procesada correctamente
def test_post_image_success(client, test_image_bytes):
    with patch("src.controller.img_controller.quality_image") as mock_quality:
        mock_quality.return_value = test_image_bytes
        data = {"file": (io.BytesIO(test_image_bytes), "test.png")}
        response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=test_Quality.png"
    assert response.content_type == "image/png"


# ✅ Imagen jfif devuelve jpg
def test_post_image_jfif_returns_jpg(client, test_image_bytes):
    with patch("src.controller.img_controller.quality_image") as mock_quality:
        mock_quality.return_value = test_image_bytes
        data = {"file": (io.BytesIO(test_image_bytes), "test.jfif")}
        response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=test_Quality.jpg"
    assert response.content_type == "image/jpeg"


# ✅ Error interno del servidor
def test_post_image_internal_error(client, test_image_bytes):
    with patch("src.controller.img_controller.quality_image") as mock_quality:
        mock_quality.side_effect = Exception("Error inesperado")
        data = {"file": (io.BytesIO(test_image_bytes), "test.png")}
        response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 500
    assert response.json["error"] == "Error interno del servidor"


# ✅ ValueError del servicio
def test_post_image_value_error(client, test_image_bytes):
    with patch("src.controller.img_controller.quality_image") as mock_quality:
        mock_quality.side_effect = ValueError("Formato inválido")
        data = {"file": (io.BytesIO(test_image_bytes), "test.png")}
        response = client.post("/img", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "Formato inválido" in response.json["error"]