import os
from datetime import datetime

from ..db.DBLogger import DBLogger
from .src.FileProcessor import FileProcessor
from .src.SiteWatcher import SiteWatcher
from .src.StopsParser import StopsParser

FILE_STOPS = ""  # path to stops.txt file
SITE_WATCHER_WAIT_TIME = 3600
STOP_CODE_COLUMN = "stop_code"
STOP_ID_COLUMN = "stop_id"
STOP_LAT_COLUMN = "stop_lat"
STOP_LON_COLUMN = "stop_lon"
STOP_NAME_COLUMN = "stop_name"
STOP_COLUMNS = ["id", "name", "lat", "lon"]
ZONE_COLUMN = "zone_id"
ZONE_TO_INCLUDE = "A"
ZTM_FILES_DIRECTORY = os.getenv("ZTM_FILES_DIRECTORY") if os.getenv("ZTM_FILES_DIRECTORY") else ""
ZTM_FILES_ENDPOINT = "https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile"

db_logger = DBLogger()
file_processor = FileProcessor(db_logger)
stops_parser = StopsParser()
site_watcher = SiteWatcher(ZTM_FILES_ENDPOINT, SITE_WATCHER_WAIT_TIME, db_logger, True)


def get_current_timestamp(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Returns the current timestamp in the provided format."""
    return datetime.now().strftime(format)
