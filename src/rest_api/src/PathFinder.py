from typing import Literal

from neo4j.graph import Path

from ...db.models.neo4j import CommutesTo, Stop
from ...db.Neo4jDBController import Neo4jDBController


class PathFinder:
    """Class responsible for finding paths in the graph representing public transportation network.

    Path is defined as `a sequence of nodes and relationships between them`."""

    QUERY_SHORTEST_PATH_LENGTH = """MATCH (start_node: $node_label)
        MATCH (end_node: $node_label)
        WHERE start_node.$node_param =~ '(?i)$start_node_param_value'
            AND end_node.$node_param =~ '(?i)$end_node_param_value'
        MATCH _shortestPath = shortestPath((start_node)-[r:$connection_label*]->(end_node))
        RETURN length(_shortestPath) as shortestPathLen
        ORDER BY shortestPathLen
        LIMIT 1
        """
    QUERY_ALL_SHORTEST_PATHS = """MATCH (start_node: $node_label)
        MATCH (end_node: $node_label)
        WHERE start_node.$node_param =~ '(?i)$start_node_param_value'
            AND end_node.$node_param =~ '(?i)$end_node_param_value'
        MATCH p = allShortestPaths((start_node)-[r:$connection_label*]->(end_node))
        $time_where_clause
        RETURN p"""

    QUERY_NAIVE_PATHS = """MATCH (start_node: $node_label)
    MATCH (end_node: $node_label)
    WHERE start_node.$node_param =~ '(?i)$start_node_param_value'
        AND end_node.$node_param =~ '(?i)$end_node_param_value'
    MATCH p = (start_node)-[r:$connection_label*$min_len..$max_len]->(end_node)
    $time_where_clause
    RETURN p
    LIMIT $paths_limit"""

    TIME_WHERE_CLAUSE = """WHERE all(line in [_rel in relationships(p)
    | $time_qualifier(line in _rel.lines where left(line, 1) = '2'
    and size(line) = 3)] where line)"""

    PATHS_LIMIT = 10

    def __init__(self, neo4j_controller: Neo4jDBController) -> None:
        self.neo4j_controller = neo4j_controller

    def find_shortest_path_len(
        self, by: Literal["code", "name"], start_point: str, end_point: str
    ) -> int:
        """Finds the length of shortest path between two given points in the public transportation network
        using the 'shortestPath' algorithm from Neo4j.

        Params:
            by: Parameter used to identify the start and end points. Can be either 'code' or 'name'.
            start_point: Value of the start point parameter, chosen in 'by' parameter.
            end_point: Value of the end point parameter, chosen in 'by' parameter."""

        if by == "code":
            node_param = Stop.CODE
        elif by == "name":
            node_param = Stop.NAME
        else:
            raise ValueError(
                "Incorrect value for 'by' parameter. Allowed values: 'code' and 'name'"
            )

        query = PathFinder.QUERY_SHORTEST_PATH_LENGTH.replace("$node_label", Stop.LABEL)
        query = query.replace("$node_param", node_param)
        query = query.replace("$start_node_param_value", start_point)
        query = query.replace("$end_node_param_value", end_point)
        query = query.replace("$connection_label", CommutesTo.LABEL)

        result = self.neo4j_controller.run_read_query(query)
        if len(result) == 1:
            return result[0]
        return None

    def find_shortest_paths(
        self,
        approach: Literal["allShortestPaths", "naive"],
        by: Literal["code", "name"],
        start_point: str,
        end_point: str,
        include_daytime: bool,
        include_nighttime: bool,
        min_len: int = 1,
    ) -> list[Path]:
        """Finds and returns all paths between two given points in the
        public transportation network using one of two possible approaches.

        Params:
            approach: Algorithm used to find the paths. Can be either 'allShortestPaths' or 'naive'.
                - 'allShortestPaths' uses the 'allShortestPaths' algorithm that comes with Neo4j.
                This approach executes fast, even on longer paths, but it doesn't catch all paths,
                even the ones that appear pretty obvious.
                - 'naive' uses a naive approach that finds X paths between two points.
                This approach executes slowly, so it's limited to the X number of paths.
                However, it catches the paths that 'allShortestPaths' misses.
            by: Parameter used to identify the start and end points. Can be either 'code' or 'name'.
            start_point: Value of the start point parameter, chosen in 'by' parameter.
            end_point: Value of the end point parameter, chosen in 'by' parameter.
            include_daytime: Bool value indicating whether daytime paths should be considered.
            include_nighttime: Bool value indicating whether nighttime paths should be considered.
            min_len: Minimum length of the path. If None passed, the value is set to 1."""

        if by == "code":
            node_param = Stop.CODE
        elif by == "name":
            node_param = Stop.NAME
        else:
            raise ValueError(
                "Incorrect value for 'by' parameter. Allowed values: 'code' and 'name'"
            )

        if approach == "allShortestPaths":
            query = PathFinder.QUERY_ALL_SHORTEST_PATHS
        else:
            query = PathFinder.QUERY_NAIVE_PATHS
            query = query.replace("$min_len", str(min_len))
            query = query.replace("$max_len", str(self._calc_max_len(min_len)))
            query = query.replace("$paths_limit", str(PathFinder.PATHS_LIMIT))

        query = query.replace("$node_label", Stop.LABEL)
        query = query.replace("$node_param", node_param)
        query = query.replace("$start_node_param_value", start_point)
        query = query.replace("$end_node_param_value", end_point)
        query = query.replace("$connection_label", CommutesTo.LABEL)

        if include_daytime and include_nighttime:
            time_where_clause = ""
            query = query.replace("$time_where_clause", "")
        else:
            if not include_daytime:
                time_qualifier = "any"
            else:
                time_qualifier = "not all"
            time_where_clause = PathFinder.TIME_WHERE_CLAUSE.replace(
                "$time_qualifier", time_qualifier
            )

        query = query.replace("$time_where_clause", time_where_clause)

        return self.neo4j_controller.run_read_query(query)

    def _calc_max_len(self, min_len: int) -> int:
        return int(min_len * 1.2 + 2)
