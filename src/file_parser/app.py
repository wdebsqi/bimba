from datetime import datetime

from . import ZTM_FILES_DIRECTORY, ZTM_FILES_ENDPOINT, db_logger, file_processor, site_watcher

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
        file_processor.unzip_file_archive(filepath, ZTM_FILES_DIRECTORY, ["stops.txt"])

    site_watcher.sleep()
