import pandas as pd

from . import (
    FILE_STOPS,
    STOP_CODE_COLUMN,
    STOP_COLUMNS,
    ZONE_COLUMN,
    ZONE_TO_INCLUDE,
    file_processor,
    stops_parser,
)

# Read and pre-process stops file
df = pd.read_csv(FILE_STOPS)  # won't work due to the lack of path in FILE_STOPS
df = file_processor.filter_on_column(df, ZONE_COLUMN, ZONE_TO_INCLUDE)
df = file_processor.remove_columns(df, [STOP_CODE_COLUMN, ZONE_COLUMN])
df = file_processor.set_columns(df, STOP_COLUMNS)

# Parse stops file to Cypher CREATE query
cypher_query = stops_parser.parse_dataframe_to_cypher_create_query(df)

print(cypher_query)
