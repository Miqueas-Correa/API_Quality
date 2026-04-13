import io
from unittest.mock import patch


# ✅ Sin archivo
def test_post_audio_no_file(client):
    response = client.post("/audio")
    assert response.status_code == 400
    assert response.json["error"] == "No se proporcionó ningún archivo"


# ✅ Archivo vacío
def test_post_audio_empty_filename(client):
    data = {"file": (io.BytesIO(b""), "")}
    response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.json["error"] == "El archivo está vacío"


# ✅ Formato no permitido
def test_post_audio_invalid_format(client):
    data = {"file": (io.BytesIO(b"fake content"), "audio.txt")}
    response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 415
    assert response.json["error"] == "Formato no permitido"


# ✅ Archivo muy grande
def test_post_audio_too_large(client, test_audio_bytes):
    large_audio = test_audio_bytes * 1000
    data = {"file": (io.BytesIO(large_audio), "audio.wav")}
    with patch.dict(client.application.config, {"AUDIO_MAX_SIZE_MB": 0.001}):
        response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 413


# ✅ Audio válido procesado correctamente
def test_post_audio_success(client, test_audio_bytes):
    with patch("src.controller.audio_controller.quality_audio") as mock_quality:
        mock_quality.return_value = test_audio_bytes
        data = {"file": (io.BytesIO(test_audio_bytes), "test.wav")}
        response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=test_Quality.wav"
    assert response.content_type == "audio/wav"


# ✅ Error interno del servidor
def test_post_audio_internal_error(client, test_audio_bytes):
    with patch("src.controller.audio_controller.quality_audio") as mock_quality:
        mock_quality.side_effect = Exception("Error inesperado")
        data = {"file": (io.BytesIO(test_audio_bytes), "test.wav")}
        response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 500
    assert response.json["error"] == "Error interno del servidor"


# ✅ ValueError del servicio
def test_post_audio_value_error(client, test_audio_bytes):
    with patch("src.controller.audio_controller.quality_audio") as mock_quality:
        mock_quality.side_effect = ValueError("Formato inválido")
        data = {"file": (io.BytesIO(test_audio_bytes), "test.wav")}
        response = client.post("/audio", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "Formato inválido" in response.json["error"]