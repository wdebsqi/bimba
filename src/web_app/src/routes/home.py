from flask import Blueprint, render_template, request

from .. import db_logger, request_logger

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET"])
def home():
    try:
        request_logger.log_request(request)
        return render_template("index.html")
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error on route /: {e}", __file__, db_logger.LOG_TYPE_ERROR
        )
