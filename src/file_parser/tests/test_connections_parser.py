class TestConnectionsParser:
    def test_connections_parser(
        self,
        connections_parser,
        example_raw_stop_times_df,
        example_raw_trips_df,
        connections_batch,
    ):
        query, batch = connections_parser.pass_dataframes(
            trips_df=example_raw_trips_df, stop_times_df=example_raw_stop_times_df
        ).parse_dataframe_to_cypher_create_query()

        print(batch)
        print(connections_batch)
        assert batch == connections_batch

    def test_class_inheritance(self, connections_parser, abstract_parser):
        assert isinstance(connections_parser, abstract_parser)
