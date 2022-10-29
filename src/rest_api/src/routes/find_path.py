from flask import Blueprint, request

from .. import db_logger, response_formatter, route_picker

bp = Blueprint("find_path", __name__)


@bp.route("/find_path", methods=["GET"])
def find_path():
    start_point_key = "start_point"
    end_point_key = "end_point"

    data = request.form

    if start_point_key not in data or end_point_key not in data:
        return f"Missing {start_point_key} or {end_point_key} parameter in request's form", 400

    if type(data[start_point_key]) != str or type(data[end_point_key]) != str:
        return f"{start_point_key} parameter and {end_point_key} must be strings", 400

    if data[start_point_key].lower() == data[end_point_key].lower():
        return "Start point and end point must be different", 400

    try:
        raw_route_data = route_picker.pick_best_route(
            "name", start_point=data[start_point_key], end_point=data[end_point_key]
        )
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error {e} encountered when picking best route",
            __file__,
            db_logger.LOG_TYPE_ERROR,
        )

    if not raw_route_data:
        return (
            f"No path found between '{data[start_point_key]}' and '{data[end_point_key]}'. "
            + "Looks like at least one of those is not a valid stop name.",
            400,
        )

    try:
        return response_formatter.format_single_route_response(raw_route_data)
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error {e} encountered when formatting the response",
            __file__,
            db_logger.LOG_TYPE_ERROR,
        )
        return 500
