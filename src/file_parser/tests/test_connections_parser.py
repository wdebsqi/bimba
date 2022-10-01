class TestConnectionsParser:
    def test_query_and_batch_creation(
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

    def test_merging_separate_connections(self, connections_parser):
        separate_connections_df = (
            connections_parser._join_source_dataframes()
            ._extract_only_necessary_columns()
            ._build_separate_connections_dataframe()
        )
        merged_df = connections_parser._merge_separate_connections(separate_connections_df)

        total_connections_in_merged = 0
        for lines_list in merged_df["lines"]:
            total_connections_in_merged += len(lines_list)

        assert total_connections_in_merged == len(separate_connections_df.index)

    def test_class_inheritance(self, connections_parser, abstract_parser):
        assert isinstance(connections_parser, abstract_parser)
