from datetime import datetime

import pandas as pd

from . import (
    ZTM_FILES_DIRECTORY,
    ZTM_FILES_ENDPOINT,
    db_logger,
    file_processor,
    neo4j_controller,
    site_watcher,
    stops_parser,
)

STOP_NODE_LABEL = "STOP"
STOPS_FILE = "stops.txt"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

db_logger.log_message("Starting the file_parser service", __file__, db_logger.LOG_TYPE_INFO)

while True:
    now = datetime.now().strftime(TIMESTAMP_FORMAT)

    print(f"{now} - Checking for new stops file...")
    db_logger.log_message("Checking for new stops file", __file__, db_logger.LOG_TYPE_INFO)

    response = site_watcher.query_site(site_watcher.HTTP_HEAD)

    new_data_available = site_watcher.check_if_new_data_available(response)
    filename = site_watcher.get_current_filename()
    print(f"New data available? {new_data_available} | Current filename: {filename}")

    if new_data_available:
        filepath = f"{ZTM_FILES_DIRECTORY}{filename}"
        file_processor.download_zip_file(ZTM_FILES_ENDPOINT, filepath)
        file_processor.unzip_file_archive(filepath, ZTM_FILES_DIRECTORY, [STOPS_FILE])
        neo4j_controller.remove_all_nodes(STOP_NODE_LABEL)
        try:
            stops_df = pd.read_csv(f"{ZTM_FILES_DIRECTORY}{STOPS_FILE}")
        except Exception as e:
            db_logger.log_message(
                f"Error while reading stops file: {e}", __file__, db_logger.LOG_TYPE_ERROR
            )
        query = stops_parser.parse_dataframe_to_cypher_create_query(stops_df)
        result = neo4j_controller.run_write_query(query)
        if result:
            db_logger.log_message(
                f"Successfully created stops. Summary: {result}", __file__, db_logger.LOG_TYPE_INFO
            )

    site_watcher.sleep()
