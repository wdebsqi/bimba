from flask import Blueprint, request

from .. import db_logger, response_formatter, route_picker

START_POINT_KEY = "start_point"
END_POINT_KEY = "end_point"
DAYTIME_LINES_KEY = "include_daytime_lines"
NIGHTTIME_LINES_KEY = "include_nighttime_lines"
REQUIRED_KEYS = [START_POINT_KEY, END_POINT_KEY, DAYTIME_LINES_KEY, NIGHTTIME_LINES_KEY]
BOOL_VALUES = {"true": True, "false": False, "True": True, "False": False, "1": True, "0": False}

bp = Blueprint("find_path", __name__)


@bp.route("/find_path", methods=["GET"])
def find_path():

    data = (
        request.form.to_dict().copy()
    )  # converting ImmutableMultiDict to Dict so that we can map the values to bools

    if not all(key in data for key in REQUIRED_KEYS):
        return (
            f"Request's form is missing at least one of the required parameters: {REQUIRED_KEYS}.",
            400,
        )

    if type(data[START_POINT_KEY]) != str or type(data[END_POINT_KEY]) != str:
        return f"{START_POINT_KEY} parameter and {END_POINT_KEY} must be strings", 400

    if data[START_POINT_KEY].lower() == data[END_POINT_KEY].lower():
        return "Start point and end point must be different", 400

    if not (data[DAYTIME_LINES_KEY] in BOOL_VALUES and data[NIGHTTIME_LINES_KEY] in BOOL_VALUES):
        return (
            f"{DAYTIME_LINES_KEY} parameter and {NIGHTTIME_LINES_KEY} must be boolean values",
            400,
        )

    data[DAYTIME_LINES_KEY] = BOOL_VALUES[data[DAYTIME_LINES_KEY]]
    data[NIGHTTIME_LINES_KEY] = BOOL_VALUES[data[NIGHTTIME_LINES_KEY]]

    if not (data[DAYTIME_LINES_KEY] or data[NIGHTTIME_LINES_KEY]):
        return (
            f"At least one has to be true: {DAYTIME_LINES_KEY} or {NIGHTTIME_LINES_KEY}",
            400,
        )

    try:
        raw_route_data = route_picker.pick_best_route(
            "name",
            start_point=data[START_POINT_KEY],
            end_point=data[END_POINT_KEY],
            include_daytime=data[DAYTIME_LINES_KEY],
            include_nighttime=data[NIGHTTIME_LINES_KEY],
        )
    except Exception as e:
        db_logger.log_message(
            f"Unidentified error {e} encountered when picking best route",
            __file__,
            db_logger.LOG_TYPE_ERROR,
        )

    if not raw_route_data:
        return (
            f"No path found between '{data[START_POINT_KEY]}' and '{data[END_POINT_KEY]}'. "
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
