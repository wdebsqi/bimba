ROUTE_STATS_LINES_CHOSEN = "lines_chosen"
ROUTE_STATS_NUM_OF_CHANGES = "num_of_changes"
ROUTE_STATS_TOTAL_STOPS = "total_stops"
STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"
STOP_NAME = "stop_name"
ZONE_ID = "zone_id"


class ResponseFormatter:
    """Class responsible for formatting the response returned to the REST API."""

    END_NODE = "end_node"
    NAME = "name"
    LAT = "lat"
    LINE_CHOSEN = "line_chosen"
    LOCATIONS = "locations"
    LON = "lon"
    PATH = "path"
    ROUTE = "route"
    START_NODE = "start_node"

    def format_single_route_response(self, route_data: dict) -> dict:
        """Formats the response from the format:
        ```
        {
            "path": <Path object>,
            "lines_chosen": <list with the lines chosen for each relationship>,
            "num_of_changes": <total number of changes in the route>
        }
        ```
        To the more developer-friendly format that can be returned by the REST API."""

        result = {self.ROUTE: [], self.LOCATIONS: []}

        for i, rel in enumerate(route_data[self.PATH].relationships):
            start_node = rel.start_node.get(STOP_NAME)
            end_node = rel.end_node.get(STOP_NAME)
            line_chosen = route_data[ROUTE_STATS_LINES_CHOSEN][i]
            result[self.ROUTE].append(
                {
                    self.START_NODE: start_node,
                    self.END_NODE: end_node,
                    self.LINE_CHOSEN: line_chosen,
                }
            )

            result[self.LOCATIONS].append(
                {
                    self.NAME: start_node,
                    self.LAT: rel.start_node.get(STOP_LAT),
                    self.LON: rel.start_node.get(STOP_LON),
                }
            )

            if i == len(route_data[self.PATH].relationships) - 1:
                result[self.LOCATIONS].append(
                    {
                        self.NAME: end_node,
                        self.LAT: rel.end_node.get(STOP_LAT),
                        self.LON: rel.end_node.get(STOP_LON),
                    }
                )

        result[ROUTE_STATS_NUM_OF_CHANGES] = route_data[ROUTE_STATS_NUM_OF_CHANGES]
        result[ROUTE_STATS_TOTAL_STOPS] = len(route_data[ROUTE_STATS_LINES_CHOSEN])
        return result
