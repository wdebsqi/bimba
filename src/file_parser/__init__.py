from .src.FileProcessor import FileProcessor
from .src.StopsParser import StopsParser

FILE_STOPS = ""  # path to stops.txt file
STOP_CODE_COLUMN = "stop_code"
STOP_ID_COLUMN = "stop_id"
STOP_LAT_COLUMN = "stop_lat"
STOP_LON_COLUMN = "stop_lon"
STOP_NAME_COLUMN = "stop_name"
STOP_COLUMNS = ["id", "name", "lat", "lon"]
ZONE_COLUMN = "zone_id"
ZONE_TO_INCLUDE = "A"

file_processor = FileProcessor()
stops_parser = StopsParser()
