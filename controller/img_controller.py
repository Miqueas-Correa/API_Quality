from flask import Blueprint, jsonify, request, send_file, current_app
import io
from service.img_service import quality_image

img_bp = Blueprint("img", __name__, url_prefix="/img")

def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("IMG_ALLOWED_EXTENSIONS", set())
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed

@img_bp.route("", methods=["POST"])
def post_image():
    try:
        max_size = current_app.config.get("IMG_MAX_SIZE_MB", 20)

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

        extension = file.filename.rsplit(".", 1)[1].lower()
        image_bytes = quality_image(file, extension)
        original_name = file.filename.rsplit(".", 1)[0]

        return send_file(
            io.BytesIO(image_bytes),
            mimetype=f"image/{extension}",
            as_attachment=True,
            download_name=f"{original_name}_Quality.{extension}"
        ), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500