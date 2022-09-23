import pandas as pd

from ...db.DBLogger import DBLogger
from ..app import STOP_NODE_LABEL
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
    def __init__(
        self, trips_df: pd.DataFrame, stop_times_df: pd.DataFrame, db_logger: DBLogger
    ) -> None:
        self.trips = trips_df
        self.stop_times = stop_times_df
        self.source_dataframe = None
        self.db_logger = db_logger

    def _join_source_dataframes(self):
        """Joins the trips and stop_times DataFrames."""
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

            for idx, row in self.source_dataframe.iterrows():
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
        return df.to_dict(orient="records")

    def parse_dataframes_to_cypher_create_query(self):
        """Runs the pipeline that produces the Cypher query and parameters
        required for the creation of the connections."""
        connections_df = (
            self._join_source_dataframes()
            ._extract_only_necessary_columns()
            ._build_connections_dataframe()
        )
        params = self._parse_connections_dataframe_to_dict(connections_df)

        query = f"""UNWIND $batch as row
        MATCH (from: {STOP_NODE_LABEL} {{stop_id: row.{RESULT_COL_FROM_STOP}}})
        MATCH (to: {STOP_NODE_LABEL} {{stop_id: row.{RESULT_COL_TO_STOP}}})
        MERGE (from)-[:commutes_to {{line: row.{RESULT_COL_LINE}}}]->(to)"""

        return query, params
