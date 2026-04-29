from flask import Flask, jsonify
from src.config import Config
from flask_cors import CORS
from src.controller.audio_controller import audio_bp
from src.controller.img_controller import img_bp
from werkzeug.exceptions import RequestEntityTooLarge
import os

def _load_config(app, config_like):
    if config_like is None:
        return
    if isinstance(config_like, dict):
        app.config.update(config_like)
        return
    try:
        app.config.from_object(config_like)
        return
    except Exception:
        try:
            app.config.from_object(config_like())
            return
        except Exception:
            try:
                app.config.update(vars(config_like))
            except Exception:
                pass

def create_app(config_class=None):
    app = Flask(__name__)

    _load_config(app, config_class)

    origins = app.config.get("CORS_ORIGINS", ["*"])
    if isinstance(origins, str):
        origins = [origins] if origins != "*" else ["*"]

    print("CORS Origins:", origins)

    CORS(
        app,
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", False),
        resources={
            r"/*": {"origins": origins},
            r"uploads/*": {"origins": origins}
        },
        allow_headers=["Content-Type", "Authorization"]
    )

    if 'MAX_CONTENT_LENGTH' not in app.config:
        size = app.config.get("AUDIO_MAX_SIZE_MB", 50)
        app.config['MAX_CONTENT_LENGTH'] = size * 1024 * 1024  # 50MB en bytes

    @app.route("/")
    def home():
        return {"message": "API funcionando"}

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(e):
        return jsonify({"error": "El archivo supera el límite permitido"}), 413

    try:
        app.register_blueprint(audio_bp)
    except Exception:
        pass
    try:
        app.register_blueprint(img_bp)
    except Exception:
        pass

    return app

if __name__ == "__main__":
    app = create_app(Config)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)