from ...db.Neo4jDBController import Neo4jDBController

STOP_CODE = "stop_code"
STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"
STOP_NAME = "stop_name"
STOP_ZONE = "zone_id"
STOP_NODE_LABEL = "STOP"


class StopsGetter:
    "Class responsible for getting the stops from the Neo4j database."
    AVAILABLE_PROPERTIES = [STOP_NAME, STOP_CODE, STOP_ZONE, STOP_LAT, STOP_LON]
    BASE_CYPHER_QUERY = "MATCH (n: $node_label) RETURN "

    def __init__(self, neo4j_db_controller: Neo4jDBController):
        self.neo4j_controller = neo4j_db_controller

    def get_all_stops(
        self,
        properties: list,
        distinct: bool = False,
        ordered: bool = False,
        ordered_by: list = None,
    ) -> list:
        """Returns a list of properties of all stops in the database."""
        for property in properties:
            if property not in self.AVAILABLE_PROPERTIES:
                raise ValueError(f"Incorrect property name '{property}'")

        query = self.BASE_CYPHER_QUERY

        if distinct:
            if not isinstance(distinct, bool):
                raise TypeError("Incorrect type for 'distinct' parameter. Must be bool.")
            query += "DISTINCT "

        return_values = ", ".join([f"n.{property}" for property in properties])
        query += return_values

        if ordered and ordered_by is not None:
            for order_property in ordered_by:
                if order_property not in properties:
                    raise ValueError(f"Cannot order by '{order_property}'")

            order_by_values = ", ".join([f"n.{order_property}" for order_property in ordered_by])
            query += f" ORDER BY {order_by_values}"

        query = query.replace("$node_label", STOP_NODE_LABEL)

        return_multiple_cols = len(properties) > 1
        return self.neo4j_controller.run_read_query(query, return_multiple_cols)
