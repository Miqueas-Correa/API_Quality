from flask import Blueprint, jsonify, request, send_file
import io
from service.img_service import quality_img

img_bp = Blueprint("img", __name__, url_prefix="/img")

# Mejorar imagen
@img_bp.route('/', methods=["POST"])
def post_img():
    try:
        if "file" not in request.files:
            return jsonify({"error":"No se proporcionó ningún archivo"}), 400
        return jsonify({
            "message":"Imagen mejorada exitosamente",
            "file": quality_img(request.files['file'])
            }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500