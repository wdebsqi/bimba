from flask import Blueprint, render_template, request

from .. import db_logger, request_logger

bp = Blueprint("error_400", __name__)


@bp.route("/error_400", methods=["GET"])
def error_400():
    try:
        start_stop = request.args.get("start_stop")
        end_stop = request.args.get("end_stop")
        request_logger.log_request(request)
        return (
            render_template(
                "error_400.html",
                start_stop=start_stop,
                end_stop=end_stop,
            ),
            400,
        )
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error on route /error_400: {e}", __file__, db_logger.LOG_TYPE_ERROR
        )
