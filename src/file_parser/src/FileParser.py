from abc import ABC, abstractmethod

import pandas as pd


class FileParser(ABC):
    @abstractmethod
    def parse_dataframe_to_cypher_create_query(self, df: pd.DataFrame) -> str:
        """Parses each row from the provided DataFrame and builds a Cypher CREATE query."""
        pass

    @abstractmethod
    def parse_row_to_cypher_node(self, row: pd.Series) -> str:
        """Iterates through a pandas Series and builds a Cypher representation of a node"""
        pass
