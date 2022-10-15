ROUTE_STATS_LINES_CHOSEN = "lines_chosen"
ROUTE_STATS_NUM_OF_CHANGES = "num_of_changes"
ROUTE_STATS_TOTAL_STOPS = "total_stops"
STOP_NAME = "stop_name"


class ResponseFormatter:
    """Class responsible for formatting the response returned to the REST API."""

    START_NODE = "start_node"
    END_NODE = "end_node"
    LINE_CHOSEN = "line_chosen"
    ROUTE = "route"

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

        result = {self.ROUTE: []}

        for i, rel in enumerate(route_data["path"].relationships):
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

        result[ROUTE_STATS_NUM_OF_CHANGES] = route_data[ROUTE_STATS_NUM_OF_CHANGES]
        result[ROUTE_STATS_TOTAL_STOPS] = len(route_data[ROUTE_STATS_LINES_CHOSEN])
        return result
