from flask import Blueprint, jsonify, request, send_file
import io
from service.audio_service import quality_audio

ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "aac", "m4a"}
MAX_SIZE_MB = 20

audio_bp = Blueprint("audio", __name__, url_prefix="/audio")

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Mejorar audio
@audio_bp.route("/", methods=["POST"])
def post_audio():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No se proporcionó ningún archivo"}), 400

        file = request.files["file"]

        if file.filename == "" or file.filename is None:
            return jsonify({"error": "El archivo está vacío"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": f"Formato no permitido"}), 415

        file.seek(0, 2)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)
        if size_mb > MAX_SIZE_MB:
            return jsonify({"error": f"El archivo supera el límite de {MAX_SIZE_MB}MB"}), 413

        audio_bytes = quality_audio(file)
        original_name = file.filename.rsplit(".", 1)[0]

        # devuelve el archivo directamente
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