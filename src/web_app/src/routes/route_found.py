import os
import requests
from flask import Blueprint, redirect, render_template, request, url_for

from .. import db_logger

bp = Blueprint("route_found", __name__)


@bp.route("/route_found", methods=["POST"])
def route_found():
    try:
        start_stop = request.form.get("start_stop")
        end_stop = request.form.get("end_stop")

        response = requests.get(
            "http://" + os.getenv("HOST") + ":5001/find_path",
            data={"start_point": start_stop, "end_point": end_stop},
        )

        if response.status_code == 200:
            response_dict = response.json()
            num_of_changes = response_dict["num_of_changes"]
            total_stops = response_dict["total_stops"]
            route = response_dict["route"]
            return render_template(
                "route_found.html",
                start_stop=start_stop,
                end_stop=end_stop,
                num_of_changes=num_of_changes,
                total_stops=total_stops,
                route=route,
            )

        return redirect(url_for("error_400.error_400", start_stop=start_stop, end_stop=end_stop))

    except Exception as e:
        db_logger.log_message(
            f"Unidentified error on route /route_found: {e}", __file__, db_logger.LOG_TYPE_ERROR
        )
