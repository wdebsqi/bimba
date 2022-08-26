class TestStopsParser:
    def test_stops_parser(self, parser, example_processed_dataframe):
        expected = (
            "CREATE \n"
            + "(:STOP {id:1234, name:'ABC', lat:1.2, lon:9.8}),\n"
            + "(:STOP {id:5678, name:'DEF', lat:2.3, lon:8.7}),\n"
            + "(:STOP {id:9012, name:'GHI', lat:3.4, lon:7.6})"
        )

        query = parser.parse_dataframe_to_cypher_create_query(example_processed_dataframe)

        assert query == expected

    def test_stops_single_row_parser(self, parser, example_processed_dataframe):
        expected = "(:STOP {id:1234, name:'ABC', lat:1.2, lon:9.8})"

        query = parser.parse_row_to_cypher_node(example_processed_dataframe.iloc[0])

        assert query == expected

    def test_class_inheritance(self, parser, abstract_parser):
        assert isinstance(parser, abstract_parser)
