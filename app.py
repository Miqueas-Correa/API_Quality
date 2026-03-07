from flask import Flask
from config import Config
from flask_cors import CORS
# importar blueprints
from controller.audio_controller import audio_bp
from controller.img_controller import img_bp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "API funcionando"}

def _load_config(app, config_like):
    if config_like is None:
        return

    # Si es un diccionario, actualizar directamente
    if isinstance(config_like, dict):
        app.config.update(config_like)
        return

    # from_object funciona con clase o instancia; usarlo y capturar errores
    try:
        app.config.from_object(config_like)
        return
    except Exception:
        # si falla, intentar instanciar (por si le pasaron la clase en vez de instancia)
        try:
            app.config.from_object(config_like())
            return
        except Exception:
            # fallback: si tiene __dict__, usarlo
            try:
                app.config.update(vars(config_like))
                return
            except Exception:
                pass

def create_app(config_class=None):
    """
    Crea la app Flask. `config_class` puede ser:
      - la clase Config (p.ej. Config)
      - una instancia Config() (p.ej. TestingConfig())
      - un dict con claves de configuración
      - None (usa defaults dentro de la app)
    """
    app = Flask(__name__)

    # cargar configuración tolerante
    _load_config(app, config_class)

    # Obtener origins de forma segura (evita KeyError)
    origins = app.config.get("CORS_ORIGINS", ["*"])
    # Asegurar que origins sea lista o "*" especial
    if isinstance(origins, str):
        origins = [origins] if origins != "*" else ["*"]

    CORS(
        app,
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True),
        resources={
            r"/*": {"origins": origins},
            r"uploads/*": {"origins": origins}
        },
        allow_headers=["Content-Type", "Authorization"]
    )

    app.config['MAX_CONTENT_LENGTH'] = app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)

    # Registrar blueprints sólo si existen (evita errores en tests parciales)
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
    # cuando se ejecuta directamente, cargar Config real si existe
    app = create_app(Config)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)