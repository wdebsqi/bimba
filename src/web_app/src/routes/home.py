from flask import Blueprint, render_template, request

from ....db.FileProcessingLogRepository import FileProcessingLogRepository
from .. import db_connector, db_logger, request_logger

bp = Blueprint("home", __name__)
file_processing_repository = FileProcessingLogRepository(db_connector)


@bp.route("/", methods=["GET"])
def home():
    try:
        request_logger.log_request(request)
        last_successful_update = file_processing_repository.get_last_successful_log().created_at

        return render_template(
            "index.html",
            last_successful_update=last_successful_update.strftime("%d-%m-%Y %H:%M:%S"),
        )
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error on route /: {e}", __file__, db_logger.LOG_TYPE_ERROR
        )
