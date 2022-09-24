class TestStopsParser:
    def test_stops_parser(self, stops_parser, example_raw_stops_dataframe):
        expected = (
            "CREATE \n"
            + "(:STOP {stop_id:1234, stop_code:'ABC1234', stop_name:'ABC', stop_lat:1.2, stop_lon:9.8, zone_id:'A'}),\n"  # noqa: E501
            + "(:STOP {stop_id:5678, stop_code:'DEF5678', stop_name:'DEF', stop_lat:2.3, stop_lon:8.7, zone_id:'B'}),\n"  # noqa: E501
            + "(:STOP {stop_id:9012, stop_code:'GHI9012', stop_name:'GHI', stop_lat:3.4, stop_lon:7.6, zone_id:'A'})"  # noqa: E501
        )
        query = stops_parser.parse_dataframe_to_cypher_create_query(example_raw_stops_dataframe)

        assert query == expected

    def test_stops_single_row_parser(self, stops_parser, example_raw_stops_dataframe):
        expected = "(:STOP {stop_id:1234, stop_code:'ABC1234', stop_name:'ABC', stop_lat:1.2, stop_lon:9.8, zone_id:'A'})"  # noqa: E501

        query = stops_parser.parse_row_to_cypher_node(example_raw_stops_dataframe.iloc[0])

        assert query == expected

    def test_class_inheritance(self, stops_parser, abstract_parser):
        assert isinstance(stops_parser, abstract_parser)
