from flask import Blueprint, render_template, request

from .. import db_logger, request_logger

bp = Blueprint("about", __name__)


@bp.route("/about", methods=["GET"])
def about():
    try:
        request_logger.log_request(request)
        return render_template("about.html")
    except Exception as e:
        db_logger.log_message(
            f"Undefined error on route /about: {e}", __file__, db_logger.LOG_TYPE_ERROR
        )
