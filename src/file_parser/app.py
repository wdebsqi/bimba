from datetime import datetime

import pandas as pd

from ..db.models import FileProcessingLog
from ..db.models.neo4j import CommutesTo, Stop
from . import (
    ZTM_FILES_DIRECTORY,
    api_handler,
    connections_parser,
    db_logger,
    file_processor,
    neo4j_controller,
    stops_parser,
)
from .src.FileHashHelper import FileHashHelper

FILE_STOP_TIMES = "stop_times.txt"
FILE_STOPS = "stops.txt"
FILE_TRIPS = "trips.txt"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

db_logger.log_message("Starting the file_parser service", __file__, db_logger.LOG_TYPE_INFO)

while True:
    now = datetime.now().strftime(TIMESTAMP_FORMAT)

    db_logger.log_message("Checking for new stops file", __file__, db_logger.LOG_TYPE_INFO)

    response = api_handler.send_request(api_handler.HTTP_GET)

    if not response:
        api_handler.sleep()
        continue

    response_filename = file_processor.read_filename_from_response_header(response)
    response_file_hash = FileHashHelper.hash_http_response_content_hash(response)

    new_data_available = api_handler.check_if_new_data_available(
        response_filename, response_file_hash
    )

    if new_data_available:
        new_file_processing_log = FileProcessingLog(
            file_name=response_filename,
            file_contents_hash=response_file_hash,
            processed_successfully=True,
        )

        filepath = f"{ZTM_FILES_DIRECTORY}{response_filename}"
        file_processor.download_zip_file(response, filepath)
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
            new_file_processing_log.processed_successfully = False
            new_file_processing_log.save()
            api_handler.sleep()
            continue

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

        new_file_processing_log.save()

    api_handler.sleep()
