from flask import Flask
from flask_cors import CORS
from app.api.routes import api
from app.config import settings
from app.logging_config import configure_logging

def create_app():
    configure_logging(settings.LOG_LEVEL)
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_UPLOAD_MB * 1024 * 1024
    CORS(app)
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def root():
        return {"name": "Automated Resume-JD ATS Matcher", "status": "running",
                "health": "/api/health"}
    return app
