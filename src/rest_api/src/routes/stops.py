from flask import Blueprint, jsonify, request

from .. import db_logger, stops_getter
from ..TypeValidator import TypeValidator

bp = Blueprint("stops", __name__)


@bp.route("/stops", methods=["GET", "POST"])
def stops():
    data_key = "properties"
    distinct_key = "distinct"
    ordered_key = "ordered"
    ordered_by_key = "ordered_by"
    data = request.get_json(silent=True)
    properties, distinct, ordered, ordered_by = None, None, None, None

    if not data:
        return "No data passed in request's body", 400

    if data_key not in data:
        return f"Missing {data_key} parameter in request's body", 400

    if not TypeValidator.validate_type(data[data_key], list):
        return f"{data_key} parameter must contain a list", 400

    properties = list(data[data_key])

    if len(data[data_key]) == 0:
        return f"{data_key} parameter must contain at least one property", 400

    properties_to_get = [
        property for property in properties if property in stops_getter.AVAILABLE_PROPERTIES
    ]

    if len(properties_to_get) == 0:
        return f"No valid properties passed in {data_key} parameter", 400

    if distinct_key in data:
        if not TypeValidator.validate_type(data[distinct_key], bool):
            return f"{distinct_key} parameter must be a bool", 400
        distinct = bool(data[distinct_key])

    if ordered_key in data and ordered_by_key in data:
        if not TypeValidator.validate_type(data[ordered_key], bool):
            return f"{ordered_key} parameter must be a bool", 400
        if not TypeValidator.validate_type(data[ordered_by_key], list):
            return f"{ordered_by_key} parameter must be a list", 400
        ordered = bool(data[ordered_key])
        ordered_by = list(data[ordered_by_key])

    try:
        return jsonify(
            stops_getter.get_all_stops(
                properties_to_get, distinct=distinct, ordered=ordered, ordered_by=ordered_by
            )
        )
    except (ValueError, TypeError) as e:
        return f"Invalid data passed in request's body: {e}", 400
    except Exception as e:
        message = f"Unidentified error {e} encountered when getting all stops"
        db_logger.log_message(
            message,
            __file__,
            db_logger.LOG_TYPE_TEST,
        )
        return message, 500
