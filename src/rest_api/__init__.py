import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .src.routes import find_path, stops

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URL").replace("\\", "")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    db.init_app(app)

    app.register_blueprint(find_path.bp)
    app.register_blueprint(stops.bp)

    return app
