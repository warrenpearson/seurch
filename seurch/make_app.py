import decimal
import enum
import secrets

from typing import Dict

from flask import Flask
from flask.json import JSONEncoder
from flask_compress import Compress
from flask_cors import CORS

# from wordsmith.adapters.monitoring import Monitoring
from seurch.config.config import config
from seurch.database import db

# celery_app = FlaskCeleryExt(create_celery_app=make_celery)


def make_app() -> Flask:
    compress = Compress()
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)
    compress.init_app(app)

    CORS(app)

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["ENV"] = config.environment

    app.json_encoder = InsigJSONEncoder

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 280}
    # app.config["CELERY_CONFIG"] = celery_config()

    db.init_app(app)
    # celery_app.init_app(app)

    # Monitoring(config).setup_app_monitoring(app)
    return app


def database_uri() -> str:
    user = config.app_database.user
    password = config.app_database.password
    host = config.app_database.host
    port = config.app_database.port
    database = config.app_database.database
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


# def celery_config() -> Dict[str, str]:
    # return {"broker_url": config.celery.broker, "result_backend": config.celery.backend}


class InsigJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(round(obj, 2))
        if isinstance(obj, enum.Enum):
            return obj.name

        try:
            return super().default(obj)
        except TypeError:
            return obj
