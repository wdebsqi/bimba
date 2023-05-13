import pandas as pd

from ...db.DBLogger import DBLogger
from ...db.models.neo4j import CommutesTo, Stop
from .FileParser import FileParser

COL_ROUTE_ID = "route_id"
COL_STOP_ID = "stop_id"
COL_STOP_SEQUENCE = "stop_sequence"
COL_TRIP_ID = "trip_id"
COLS_SOURCE_DF = [COL_TRIP_ID, COL_STOP_ID, COL_STOP_SEQUENCE, COL_ROUTE_ID]
RESULT_COL_FROM_STOP = "from_stop"
RESULT_COL_TO_STOP = "to_stop"
RESULT_COL_LINE = "line"
RESULT_COL_LINES = "lines"
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

    def _build_separate_connections_dataframe(self) -> pd.DataFrame | None:
        """Builds a DataFrame containing the data about separate connections.
        Each row of the DataFrame represents a single connection between two stops for a given line.
        Example DataFrame may look like this:

        | id | from_stop | to_stop | line |
        |:--:|:---------:|:-------:|:----:|
        | 0  | 1143      | 4145    | A    |
        | 1  | 4145      | 1925    | B    |
        | 2  | 1925      | 2969    | B    |
        | 3  | 1143      | 4145    | C    |
        | 4  | 4145      | 1925    | C    |"""
        if self.source_dataframe is None:
            self.db_logger.log_message(
                "Source DataFrame is None. Can't extract necessary columns.",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
            return None

        result_dict = {RESULT_COL_FROM_STOP: [], RESULT_COL_TO_STOP: [], RESULT_COL_LINE: []}
        lines_available = self.source_dataframe[COL_ROUTE_ID].unique()

        for line in lines_available:
            line_df = self.source_dataframe[self.source_dataframe[COL_ROUTE_ID] == line]

            for idx, row in line_df.iloc[1:, :].iterrows():
                if row[COL_STOP_SEQUENCE] == 0:
                    continue

                prev_row = self.source_dataframe.iloc[idx - 1]
                result_dict[RESULT_COL_FROM_STOP].append(prev_row[COL_STOP_ID])
                result_dict[RESULT_COL_TO_STOP].append(row[COL_STOP_ID])
                result_dict[RESULT_COL_LINE].append(str(prev_row[COL_ROUTE_ID]))

        result_df = pd.DataFrame.from_dict(result_dict)
        return result_df.drop_duplicates().reset_index(drop=True)

    def _merge_separate_connections(self, separate_connections_df: pd.DataFrame) -> pd.DataFrame:
        """Merges the DataFrame containing the data about separate connections.
        Each row of the result DataFrame represents a single connection between two stops.
        The lines commuting between two stops are merged into a list, stored in the 'lines' column.
        Example DataFrame may look like this:
        | id | from_stop | to_stop | lines |
        |:--:|:---------:|:-------:|:-----:|
        | 0  | 1143      | 4145    | [A, C]|
        | 1  | 4145      | 1925    | [B, C]|
        | 2  | 1925      | 2969    | [B]   |"""
        separate_connections_first_row = separate_connections_df.iloc[0]
        result_df = pd.DataFrame(
            {
                RESULT_COL_FROM_STOP: [separate_connections_first_row[RESULT_COL_FROM_STOP]],
                RESULT_COL_TO_STOP: [separate_connections_first_row[RESULT_COL_TO_STOP]],
                RESULT_COL_LINE: [[separate_connections_first_row[RESULT_COL_LINE]]],
            }
        )

        for i in range(1, len(separate_connections_df.index)):
            row_to_check = separate_connections_df.iloc[i].astype(object)
            rows_with_same_stops = result_df[
                (result_df[RESULT_COL_FROM_STOP] == row_to_check[RESULT_COL_FROM_STOP])
                & (result_df[RESULT_COL_TO_STOP] == row_to_check[RESULT_COL_TO_STOP])
            ]
            found_same_stops_for_the_row = len(rows_with_same_stops.index) > 0

            if found_same_stops_for_the_row:
                idx = rows_with_same_stops.iloc[0].name
                result_df.at[idx, RESULT_COL_LINE].append(row_to_check[RESULT_COL_LINE])
            else:
                row_to_check.at[RESULT_COL_LINE] = [row_to_check[RESULT_COL_LINE]]
                result_df = pd.concat([result_df, row_to_check.to_frame().T])

        result_df.columns = [RESULT_COL_FROM_STOP, RESULT_COL_TO_STOP, RESULT_COL_LINES]
        result_df[RESULT_COL_FROM_STOP] = result_df[RESULT_COL_FROM_STOP].astype(int)
        result_df[RESULT_COL_TO_STOP] = result_df[RESULT_COL_TO_STOP].astype(int)
        return result_df

    def _parse_connections_dataframe_to_dict(self, df: pd.DataFrame | None) -> dict | None:
        """Parses the connections DataFrame to a dictionary that can be used
        as a parameter in Cypher query."""
        if df is None:
            self.db_logger.log_message(
                """Parameters DataFrame is None. Make sure that the '_build_separate_connections_dataframe'
                and '_merge_separate_connections' methods have been called before.""",
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
        separate_connections_df = (
            self._join_source_dataframes()
            ._extract_only_necessary_columns()
            ._build_separate_connections_dataframe()
        )
        merged_df = self._merge_separate_connections(separate_connections_df)
        params = self._parse_connections_dataframe_to_dict(merged_df)

        if params is None:
            self.db_logger.log_message(
                """Parameters dictionary is empty. Make sure that the
                '_parse_connections_dataframe_to_dict' method has been called before.""",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )
            return None
        query = f"""UNWIND $batch as row
        MATCH (from: {Stop.LABEL} {{{COL_STOP_ID}: row.{RESULT_COL_FROM_STOP}}})
        MATCH (to: {Stop.LABEL} {{{COL_STOP_ID}: row.{RESULT_COL_TO_STOP}}})
        MERGE (from)-[:{CommutesTo.LABEL} {{{RESULT_COL_LINES}: row.{RESULT_COL_LINES}}}]->(to)"""  # noqa: E501

        return query, params

    def parse_row_to_cypher_node(self) -> None:
        """Added for compatibility with the parent class."""
        pass
