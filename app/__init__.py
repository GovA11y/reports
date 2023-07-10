# app/__init__.py

from flask import Flask
from app.api.domain.views import domain_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(domain_bp)

    return app