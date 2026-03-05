from flask import Blueprint, jsonify, request, send_file
import io
from service.audio_service import quality_audio

audio_bp = Blueprint("audio", __name__, url_prefix="/audio")

# Modificar audio
@audio_bp.route('/', methods=["POST"])
def post_audio():
    try:
        if not request.files['file']:
            return jsonify({"error":"No se proporcionó ningún archivo"}), 400
        return jsonify({
            "message":"Audio modificado exitosamente",
            "file": quality_audio(request.files['file'])
            }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500