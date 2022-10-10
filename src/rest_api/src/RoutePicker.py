from typing import Literal

import pandas as pd
from neo4j.graph import Relationship

from . import RELATION_LINES_LABEL, ROUTE_STATS_LINES_CHOSEN, ROUTE_STATS_NUM_OF_CHANGES
from .LinePicker import LinePicker
from .PathFinder import PathFinder


class RoutePicker:
    """Class responsible for picks the best route for the given starting point and ending point.

    Route is defined as `a sequence of stops and their corresponding lines
    that the user should take`."""

    def __init__(self, path_finder: PathFinder, line_picker: LinePicker) -> None:
        self.path_finder = path_finder
        self.line_picker = line_picker

    def pick_best_route(
        self, by: Literal["code", "name"], start_point: str, end_point: str
    ) -> dict:
        """Finds all paths between start_point and end_point using allShortestPaths
        algorithm, processes them and returns a dictionary looking like this:
        ```
        {
            "path": <Path object>,
            "lines_chosen": <list with the lines chosen for each relationship>,
            "num_of_changes": <total number of changes in the route>
        }
        ```"""
        all_shortest_paths = self.path_finder.find_all_shortest_paths(
            by=by, start_point=start_point, end_point=end_point
        )

        if not all_shortest_paths:
            return None

        routes_data = dict.fromkeys(all_shortest_paths)

        # iterates through every path
        for path in all_shortest_paths:
            lines_chosen = []
            lines_occurences = self._count_lines_occurences(path.relationships)

            for i, rel in enumerate(path.relationships):
                lines_available = rel.get(RELATION_LINES_LABEL)

                # try to continue using the previous line
                if i != 0:
                    # previous_rel = path.relationships[i - 1]
                    previous_line = lines_chosen[i - 1]
                    if previous_line in lines_available:
                        lines_chosen.append(previous_line)
                        continue

                # pick the best line if continuing with the previous line unavailable
                lines_chosen.append(
                    self.line_picker.choose_most_occuring_line(lines_occurences, lines_available)
                )

            # count the number of changes in the route
            num_of_changes = self._count_num_of_changes(lines_chosen)

            # save the data for the route in the dictionary
            route_data = {
                ROUTE_STATS_LINES_CHOSEN: lines_chosen,
                ROUTE_STATS_NUM_OF_CHANGES: num_of_changes,
            }
            routes_data[path] = route_data

        return self._pick_best_route(routes_data)

    def _pick_best_route(self, routes_data: dict) -> dict:
        """Picks the best route from the given dictionary containing
        data about multiple available routes."""
        result = None
        for path, data in routes_data.items():
            if (
                result is None
                or data[ROUTE_STATS_NUM_OF_CHANGES] < result[ROUTE_STATS_NUM_OF_CHANGES]
            ):
                result = {
                    "path": path,
                    ROUTE_STATS_LINES_CHOSEN: data[ROUTE_STATS_LINES_CHOSEN],
                    ROUTE_STATS_NUM_OF_CHANGES: data[ROUTE_STATS_NUM_OF_CHANGES],
                }

        return result

    def _count_lines_occurences(self, relationships: list[Relationship]) -> pd.Series:
        """Counts how many times each line occurs in the stops on the path
        and returns the Pandas Series sorted in descending order."""
        lines = [rel.get(RELATION_LINES_LABEL) for rel in relationships]
        unique_lines = set([line for lines_list in lines for line in lines_list])
        lines_counter = dict.fromkeys(unique_lines, 0)

        for lines_list in lines:
            for line in lines_list:
                lines_counter[line] += 1

        lines_counter_ser = pd.Series(lines_counter)
        return lines_counter_ser.sort_values(ascending=False)

    def _count_num_of_changes(self, lines_chosen: list[str]) -> int:
        """Counts the total number of changes in the route."""
        if len(lines_chosen) <= 1:
            return 0

        result = 0
        for i, line in enumerate(lines_chosen[1:], 1):
            previous_line = lines_chosen[i - 1]
            if line != previous_line:
                result += 1

        return result
