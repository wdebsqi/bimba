import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .src.routes import error_400, home, route_found

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="src/views", static_folder="src/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URL").replace("\\", "")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    db.init_app(app)

    app.register_blueprint(home.bp)
    app.register_blueprint(route_found.bp)
    app.register_blueprint(error_400.bp)

    return app
