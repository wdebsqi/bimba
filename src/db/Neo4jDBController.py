from neo4j import GraphDatabase, SummaryCounters
from neo4j.exceptions import AuthError, TransactionError

from . import DBLogger

LABELS_ADDED = "labels_added"
LABELS_REMOVED = "labels_removed"
NODES_CREATED = "nodes_created"
NODES_DELETED = "nodes_deleted"
PROPERTIES_SET = "properties_set"
RELATIONSHIPS_CREATED = "relationships_created"
RELATIONSHIPS_DELETED = "relationships_deleted"


class Neo4jDBController:
    def __init__(self, uri: str, user: str, password: str, db_logger: DBLogger) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.db_logger = db_logger

    def close(self) -> None:
        """Closes the connection to the Neo4j database."""
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def ping(self) -> bool:
        """Pings the database and returns True if the ping was successful."""
        with self.driver.session(database="neo4j") as session:
            try:
                session.run("match (n) return n limit 1")
                return True
            except AuthError as ae:
                self.db_logger.log_message(
                    f"Failed to authenticate to Neo4j: {ae}",
                    __file__,
                    self.db_logger.LOG_TYPE_ERROR,
                )
                return False
            except Exception as e:
                self.db_logger.log_message(
                    f"Unidentified error when pinging Neo4j: {e}",
                    __file__,
                    self.db_logger.LOG_TYPE_ERROR,
                )
                return False

    def remove_all_nodes(self, node_type: str) -> int:
        """Removes all nodes of a given type and returns the number of removed rows."""
        try:
            with self.driver.session() as session:
                result = session.write_transaction(self._remove_all_nodes, node_type)
                if result > 0:
                    self.db_logger.log_message(
                        f"Successfully removed {result} nodes of type {node_type}",
                        __file__,
                        self.db_logger.LOG_TYPE_INFO,
                    )
                else:
                    self.db_logger.log_message(
                        f"Removed 0 nodes of type {node_type}. Check if the node type was correct.",
                        __file__,
                        self.db_logger.LOG_TYPE_DEBUG,
                    )

                return result

        except TransactionError as te:
            self.db_logger.log_message(
                f"Transaction error: {te} when trying to remove all nodes of type {node_type}",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )

        except Exception as e:
            self.db_logger.log_message(
                f"Unidentified error when removing all nodes of type {node_type}: {e}",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )

    @staticmethod
    def _remove_all_nodes(tx, node_type: str) -> int:
        """Removes all nodes of a given type and returns the number of removed nodes."""
        result = tx.run(f"MATCH (n:{node_type}) DETACH DELETE n")
        summary = result.consume()
        return Neo4jDBController._extract_values_from_counters(summary.counters, [NODES_DELETED])[
            NODES_DELETED
        ]

    def run_write_query(self, query: str, **params) -> dict:
        """Runs a provided write query with the optional parameters and returns the summary."""
        try:
            with self.driver.session() as session:
                result = session.write_transaction(self._run_write_query, query, params)
                return result

        except TransactionError as te:
            self.db_logger.log_message(
                f"Transaction error: {te} occured when trying to run a write query: {query}",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )

        except Exception as e:
            self.db_logger.log_message(
                f"Unidentified error: {e} occured when trying to run a write query: {query}",
                __file__,
                self.db_logger.LOG_TYPE_ERROR,
            )

    @staticmethod
    def _run_write_query(tx, query: str, params: dict) -> dict:
        """Runs a provided write query with the optional parameters
        and returns the result summary."""
        result = tx.run(query, params)
        summary = result.consume()
        return Neo4jDBController._extract_values_from_counters(summary.counters)

    @staticmethod
    def _extract_values_from_counters(
        counters: SummaryCounters, values_to_extract: list = None
    ) -> dict:
        """Parses an instance of neo4j.SummaryCounters to a dict and returns it.
        values_to_extract is a list of values that will be extracted from the SummaryCounters object
        (if not specified, all values will be extracted).
        SummaryCounters is a class that contains quantitative summary about a query ran.
        You can read more about neo4j.SummaryCounters here:
        https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.SummaryCounters"""

        base_map = {
            NODES_CREATED: counters.nodes_created,
            NODES_DELETED: counters.nodes_deleted,
            RELATIONSHIPS_CREATED: counters.relationships_created,
            RELATIONSHIPS_DELETED: counters.relationships_deleted,
            PROPERTIES_SET: counters.properties_set,
            LABELS_ADDED: counters.labels_added,
            LABELS_REMOVED: counters.labels_removed,
        }

        if values_to_extract is None:
            return base_map

        return {
            k: v for k, v in base_map.items() if k in values_to_extract and k in base_map.keys()
        }
