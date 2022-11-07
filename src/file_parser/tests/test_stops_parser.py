from ...db.models.neo4j import Stop


class TestStopsParser:
    def test_stops_parser(self, stops_parser, example_raw_stops_dataframe):
        expected = (
            "CREATE \n"
            + f"(:{Stop.LABEL} {{{Stop.ID}:1234, {Stop.CODE}:'ABC1234', {Stop.NAME}:'ABC', {Stop.LAT}:1.2, {Stop.LON}:9.8, {Stop.ZONE}:'A'}}),\n"  # noqa: E501
            + f"(:{Stop.LABEL} {{{Stop.ID}:5678, {Stop.CODE}:'DEF5678', {Stop.NAME}:'DEF', {Stop.LAT}:2.3, {Stop.LON}:8.7, {Stop.ZONE}:'B'}}),\n"  # noqa: E501
            + f"(:{Stop.LABEL} {{{Stop.ID}:9012, {Stop.CODE}:'GHI9012', {Stop.NAME}:'GHI', {Stop.LAT}:3.4, {Stop.LON}:7.6, {Stop.ZONE}:'A'}})"  # noqa: E501
        )
        query = stops_parser.parse_dataframe_to_cypher_create_query(example_raw_stops_dataframe)

        assert query == expected

    def test_stops_single_row_parser(self, stops_parser, example_raw_stops_dataframe):
        expected = f"(:{Stop.LABEL} {{{Stop.ID}:1234, {Stop.CODE}:'ABC1234', {Stop.NAME}:'ABC', {Stop.LAT}:1.2, {Stop.LON}:9.8, {Stop.ZONE}:'A'}})"  # noqa: E501

        query = stops_parser.parse_row_to_cypher_node(example_raw_stops_dataframe.iloc[0])

        assert query == expected

    def test_class_inheritance(self, stops_parser, abstract_parser):
        assert isinstance(stops_parser, abstract_parser)
