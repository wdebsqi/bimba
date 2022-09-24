import pandas as pd

from ...db.DBLogger import DBLogger
from . import STOP_CONNECTIONS_LABEL, STOP_NODE_LABEL
from .FileParser import FileParser

COL_ROUTE_ID = "route_id"
COL_STOP_ID = "stop_id"
COL_STOP_SEQUENCE = "stop_sequence"
COL_TRIP_ID = "trip_id"
COLS_SOURCE_DF = [COL_TRIP_ID, COL_STOP_ID, COL_STOP_SEQUENCE, COL_ROUTE_ID]
RESULT_COL_FROM_STOP = "from_stop"
RESULT_COL_TO_STOP = "to_stop"
RESULT_COL_LINE = "line"
RESULT_COLS_DF = [RESULT_COL_FROM_STOP, RESULT_COL_TO_STOP, RESULT_COL_LINE]


class ConnectionsParser(FileParser):
    def __init__(self, db_logger: DBLogger = None) -> None:
        self.trips = None
        self.stop_times = None
        self.source_dataframe = None
        self.db_logger = db_logger

    def pass_dataframes(self, trips_df: pd.DataFrame, stop_times_df: pd.DataFrame):
        """Passes the required DataFrames to the parser.
        'trips_df' should be the DataFrame created from 'trips.csv' file.
        'stop_times_df' should be the DataFrame created from 'stop_times.csv' file."""
        self.trips = trips_df
        self.stop_times = stop_times_df
        return self

    def _join_source_dataframes(self):
        """Joins the trips and stop_times DataFrames."""
        if self.trips is None or self.stop_times is None:
            self.db_logger.log_message(
                """'trips' DataFrame or 'stop_times' DataFrame not passed to the object.
                    Make sure that the 'pass_dataframes' method has been called before.""",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
        else:
            self.source_dataframe = self.stop_times.merge(self.trips, on=COL_TRIP_ID)
        return self

    def _extract_only_necessary_columns(self):
        """Extracts only the columns needed for building the query."""
        if self.source_dataframe is None:
            self.db_logger.log_message(
                "Source DataFrame is None. Can't extract necessary columns.",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
        else:
            self.source_dataframe = self.source_dataframe[COLS_SOURCE_DF]
        return self

    def _build_connections_dataframe(self):
        """Builds the DataFrame containing the connections data."""
        if self.source_dataframe is None:
            self.db_logger.log_message(
                "Source DataFrame is None. Can't extract necessary columns.",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
            return None
        else:
            result_dict = {RESULT_COL_FROM_STOP: [], RESULT_COL_TO_STOP: [], RESULT_COL_LINE: []}
            result_df = pd.DataFrame.from_dict(result_dict)
            lines_available = self.source_dataframe[COL_ROUTE_ID].unique()

            for line in lines_available:
                line_df = self.source_dataframe[self.source_dataframe[COL_ROUTE_ID] == line]

                for idx, row in line_df.iloc[1:, :].iterrows():
                    if row[COL_STOP_SEQUENCE] == 0:
                        continue

                    prev_row = self.source_dataframe.iloc[idx - 1]
                    result_dict[RESULT_COL_FROM_STOP].append(prev_row[COL_STOP_ID])
                    result_dict[RESULT_COL_TO_STOP].append(row[COL_STOP_ID])
                    result_dict[RESULT_COL_LINE].append(prev_row[COL_ROUTE_ID])

            result_df = pd.DataFrame.from_dict(result_dict)
            return result_df.drop_duplicates().reset_index(drop=True)

    def _parse_connections_dataframe_to_dict(self, df):
        """Parses the connections DataFrame to a dictionary that can be used
        as a parameter in Cypher query."""
        if df is None:
            self.db_logger.log_message(
                """Parameters DataFrame is None. Make sure that the
                '_build_connections_dataframe' method has been called before.""",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
            return None
        return df.to_dict(orient="records")

    def parse_dataframe_to_cypher_create_query(self):
        """Runs the pipeline that produces the Cypher query and parameters
        required for the creation of the connections.
        Requires passing the trips and stop_times DataFrames before
        (call 'pass_dataframes' method and pass them as the parameters)."""
        connections_df = (
            self._join_source_dataframes()
            ._extract_only_necessary_columns()
            ._build_connections_dataframe()
        )
        params = self._parse_connections_dataframe_to_dict(connections_df)

        if params is None:
            self.db_logger.log_message(
                """Parameters dictionary is empty. Make sure that the
                '_parse_connections_dataframe_to_dict' method has been called before.""",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
            return None
        query = f"""UNWIND $batch as row
        MATCH (from: {STOP_NODE_LABEL} {{{COL_STOP_ID}: row.{RESULT_COL_FROM_STOP}}})
        MATCH (to: {STOP_NODE_LABEL} {{{COL_STOP_ID}: row.{RESULT_COL_TO_STOP}}})
        MERGE (from)-[:{STOP_CONNECTIONS_LABEL} {{line: row.{RESULT_COL_LINE}}}]->(to)"""

        return query, params

    def parse_row_to_cypher_node(self) -> None:
        """Added for compatibility with the parent class."""
        pass
