from __future__ import annotations


import os
from typing import Mapping, Any
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from .config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
app = Flask(__name__)
app.config.from_object(Config)
if config_overrides:
app.config.update(dict(config_overrides))


os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)


db.init_app(app)
migrate.init_app(app, db)


api = Api(app) # Swagger at /docs


# dev static for media
from .__init__media_static_patch import register_media_route
register_media_route(app)


# ---- register blueprints ----
from .api.tweets import blp as tweets_blp
from .api.users import blp as users_blp
from .api.medias import blp as medias_blp


api.register_blueprint(tweets_blp, url_prefix="/api/tweets")
api.register_blueprint(users_blp, url_prefix="/api/users")
api.register_blueprint(medias_blp, url_prefix="/api/medias")


@app.get("/ping")
def ping():
return {"result": True, "message": "pong"}


@app.errorhandler(Exception)
def handle_error(e):
# Единый формат ошибки по ТЗ
return jsonify({"result": False, "error_type": type(e).__name__, "error_message": str(e)}), 400


return app


# импорт моделей для Alembic автогенерации
from . import models # noqa: E402,WPS300