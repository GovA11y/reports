# Relative Path: app/api/__init__.py
from flask import Flask
from .domain.views import domain_bp
from .axe.views import axe_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(domain_bp)
    app.register_blueprint(axe_bp)

    return app