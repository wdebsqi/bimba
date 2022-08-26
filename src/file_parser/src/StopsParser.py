import pandas as pd
from .FileParser import FileParser

CYPHER_CREATE_BEGINNING = "CREATE \n"
CYPHER_NODE_STOP_BEGINNING = "(:STOP {"


class StopsParser(FileParser):
    """Handles parsing data from the provided DataFrame to Cypher queries."""

    def parse_dataframe_to_cypher_create_query(self, df: pd.DataFrame) -> str:
        """Parses each row from the provided DataFrame and builds a Cypher CREATE query."""

        query = CYPHER_CREATE_BEGINNING
        for index, row in df.iterrows():
            new_node_entry = self.parse_row_to_cypher_node(row)
            query += new_node_entry

            if index != df.iloc[-1].name:
                query += ",\n"

        return query

    def parse_row_to_cypher_node(self, row: pd.Series) -> str:
        """Iterates through a pandas Series and builds a Cypher representation of a STOP node"""

        node_entry = CYPHER_NODE_STOP_BEGINNING
        for i in range(len(row)):
            col_name = row.index[i]
            col_value = row[col_name]
            if not self._is_digit(col_value):
                col_value = f"'{col_value}'"

            node_entry += f"{col_name}:{col_value}"

            if i != len(row) - 1:
                node_entry += ", "

        node_entry += "})"

        return node_entry

    def _is_digit(self, text: str) -> bool:
        """Checks if the text provided can be parsed to a digit."""
        try:
            return bool(int(text))
        except ValueError:
            return False
