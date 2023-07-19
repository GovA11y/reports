# app/__init__.py
import os
from dotenv import load_dotenv
import pyroscope
from flask import Flask
from app.api.domain.views import domain_bp
from app.api.axe.views import axe_bp
from app.api.activity.views import activity_bp
from app.api.metrics.views import metrics_bp
from app.api.utils import start_scheduled_jobs
from app.logging import logger

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(domain_bp)
    app.register_blueprint(axe_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(metrics_bp)

    return app


def configure_pyroscope():
    # Configure Pyroscope
    pyroscope.configure(
        application_name=os.getenv("PYROSCOPE_APPLICATION_NAME"),
        server_address=os.getenv("PYROSCOPE_SERVER"),
    )





def startup():
    start_scheduled_jobs()
    configure_pyroscope()
