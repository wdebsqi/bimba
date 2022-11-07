from datetime import datetime

import pandas as pd

from ..db.models.neo4j import CommutesTo, Stop
from . import (
    ZTM_FILES_DIRECTORY,
    ZTM_FILES_ENDPOINT,
    connections_parser,
    db_logger,
    file_processor,
    neo4j_controller,
    site_watcher,
    stops_parser,
)

FILE_STOP_TIMES = "stop_times.txt"
FILE_STOPS = "stops.txt"
FILE_TRIPS = "trips.txt"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

db_logger.log_message("Starting the file_parser service", __file__, db_logger.LOG_TYPE_INFO)

while True:
    now = datetime.now().strftime(TIMESTAMP_FORMAT)

    db_logger.log_message("Checking for new stops file", __file__, db_logger.LOG_TYPE_INFO)

    response = site_watcher.query_site(site_watcher.HTTP_HEAD)

    if not response:
        site_watcher.sleep()
        continue

    new_data_available = site_watcher.check_if_new_data_available(response)
    filename = site_watcher.get_current_filename()

    if new_data_available:
        filepath = f"{ZTM_FILES_DIRECTORY}{filename}"
        file_processor.download_zip_file(ZTM_FILES_ENDPOINT, filepath)
        file_processor.unzip_file_archive(
            filepath, ZTM_FILES_DIRECTORY, [FILE_STOPS, FILE_STOP_TIMES, FILE_TRIPS]
        )

        # reading files
        try:
            stops_df = pd.read_csv(f"{ZTM_FILES_DIRECTORY}{FILE_STOPS}")
            stop_times_df = pd.read_csv(f"{ZTM_FILES_DIRECTORY}{FILE_STOP_TIMES}")
            trips_df = pd.read_csv(f"{ZTM_FILES_DIRECTORY}{FILE_TRIPS}")
        except Exception as e:
            db_logger.log_message(
                f"Error while reading ZTM files: {e}", __file__, db_logger.LOG_TYPE_ERROR
            )
            site_watcher.sleep()

        # parsing stops
        query = stops_parser.parse_dataframe_to_cypher_create_query(stops_df)
        neo4j_controller.remove_all_nodes(Stop.LABEL)
        result = neo4j_controller.run_write_query(query)
        if result:
            db_logger.log_message(
                f"Successfully created stops. Summary: {result}", __file__, db_logger.LOG_TYPE_INFO
            )

        # parsing connections
        query, batch = connections_parser.pass_dataframes(
            trips_df=trips_df, stop_times_df=stop_times_df
        ).parse_dataframe_to_cypher_create_query()
        neo4j_controller.remove_all_connections(CommutesTo.LABEL)
        result = neo4j_controller.run_write_query(query, batch=batch)
        if result:
            db_logger.log_message(
                f"Successfully created connections. Summary: {result}",
                __file__,
                db_logger.LOG_TYPE_INFO,
            )

    site_watcher.sleep()
