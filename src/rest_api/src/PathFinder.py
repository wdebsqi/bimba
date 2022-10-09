from typing import Literal

from neo4j.graph import Path

from ...db.DBLogger import DBLogger
from ...db.Neo4jDBController import Neo4jDBController
from . import STOP_CODE, STOP_CONNECTIONS_LABEL, STOP_NAME, STOP_NODE_LABEL


class PathFinder:
    """Class responsible for finding paths in the graph representing public transportation network.

    Path is defined as `a sequence of nodes and relationships between them`."""

    QUERY_ALL_SHORTEST_PATHS = """MATCH (start_node: $node_label {$node_param: '$start_node_param_value'})
        MATCH (end_node: $node_label {$node_param: '$end_node_param_value'})
        MATCH p = allShortestPaths((start_node)-[r:$connection_label*]->(end_node))
        RETURN p"""

    def __init__(self, neo4j_controller: Neo4jDBController, db_logger: DBLogger) -> None:
        self.neo4j_controller = neo4j_controller
        self.db_logger = db_logger

    def find_all_shortest_paths(
        self, by: Literal["code", "name"], start_point: str, end_point: str
    ) -> list[Path]:
        """Finds and returns all paths between two given points in the public transportation network
        using the 'allShortestPaths' algorithm from Neo4j.

        Params:
            by: Parameter used to identify the start and end points. Can be either 'code' or 'name'.
            start_point: Value of the start point parameter, chosen in 'by' parameter.
            end_point: Value of the end point parameter, chosen in 'by' parameter."""

        if by == "code":
            node_param = STOP_CODE
        elif by == "name":
            node_param = STOP_NAME
        else:
            raise ValueError(
                "Incorrect value for 'by' parameter. Allowed values: 'code' and 'name'"
            )

        query = PathFinder.QUERY_ALL_SHORTEST_PATHS.replace("$node_label", STOP_NODE_LABEL)
        query = query.replace("$node_param", node_param)
        query = query.replace("$start_node_param_value", start_point)
        query = query.replace("$end_node_param_value", end_point)
        query = query.replace("$connection_label", STOP_CONNECTIONS_LABEL)

        return self.neo4j_controller.run_read_query(query)
