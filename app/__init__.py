# app/__init__.py
import os
import socket
import platform
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
    logger.info('Configuring Pyroscope')
    host = socket.gethostname()
    platform_info = platform.platform()
    python_version = platform.python_version()
    host_os = platform.system()
    host_os_release = platform.release()
    host_os_version = platform.version()
    host_machine_type = platform.machine()
    host_processor = platform.processor()
    python_implementation = platform.python_implementation()
    python_compiler = platform.python_compiler()
    python_build = platform.python_build()
    logger.debug('Pyroscope Vars Imported, Now Setting Tags...')
    tags = {
        "host": host,
        "platform_info": platform_info,
        "python_version": python_version,
        "host_os": host_os,
        "host_os_release": host_os_release,
        "host_os_version": host_os_version,
        "host_machine_type": host_machine_type,
        "host_processor": host_processor,
        "python_implementation": python_implementation,
        "python_compiler": python_compiler,
        "python_build": python_build,
    }
    logger.debug('Pyroscope Tags Set')
    pyroscope.configure(
        application_name=os.getenv("PYROSCOPE_APPLICATION_NAME"),
        server_address=os.getenv("PYROSCOPE_SERVER"),
        auth_token=os.getenv("PYROSCOPE_API_KEY"),
        sample_rate=100,
        detect_subprocesses=True,
        oncpu=False,
        native=True,
        gil_only=True,
        log_level=os.getenv("LOG_LEVEL"),
        tags=tags,
    )
    logger.info('Pyroscope Configured')




def startup():
    configure_pyroscope()
    logger.info('Starting Scheduled Jobs')
    start_scheduled_jobs()
    logger.info('Scheduled Jobs Started')
