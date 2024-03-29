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
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

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
    logger.debug('Pyroscope Vars Imported...')

    pyroscope.configure(
        application_name=os.getenv("PYROSCOPE_APPLICATION_NAME"),
        server_address=os.getenv("PYROSCOPE_SERVER"),
        auth_token=os.getenv("PYROSCOPE_API_KEY"),
    )
    logger.info('Pyroscope Configured')


def traces_sampler(sampling_context):
    # Customize your sampling logic here if needed
    # return a number between 0 and 1 or a boolean
    return 1.0


def configure_sentry():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN_REPORTS"),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        traces_sampler=traces_sampler  # Optional if you want dynamic sampling
    )


def startup():
    configure_pyroscope()
    configure_sentry()
    logger.info('Sentry Configured')
    logger.info('Starting Scheduled Jobs')
    start_scheduled_jobs()
    logger.info('Scheduled Jobs Started')
