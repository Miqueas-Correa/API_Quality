from flask import Blueprint, jsonify, request, send_file, current_app
import io
from src.service.audio_service import quality_audio

audio_bp = Blueprint("audio", __name__, url_prefix="/audio")

def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("AUDIO_ALLOWED_EXTENSIONS") or {"mp3", "wav", "ogg", "flac", "aac", "m4a"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed

@audio_bp.route("", methods=["POST"])
def post_audio():
    try:
        max_size = current_app.config.get("AUDIO_MAX_SIZE_MB", 5)

        if "file" not in request.files:
            return jsonify({"error": "No se proporcionó ningún archivo"}), 400

        file = request.files["file"]

        if file.filename == "" or file.filename is None:
            return jsonify({"error": "El archivo está vacío"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Formato no permitido"}), 415

        file.seek(0, 2)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)
        if size_mb > max_size:
            return jsonify({"error": f"El archivo supera el límite de {max_size}MB"}), 413

        audio_bytes = quality_audio(file)
        original_name = file.filename.rsplit(".", 1)[0]

        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"{original_name}_Quality.wav"
        ), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500