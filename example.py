import logging
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, TransactionError

# Loading environment variables from .env file
load_dotenv()
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name
            )
            for row in result:
                print(f"Created friendship between {row['p1']} and {row['p2']}")

    @staticmethod
    def _create_and_return_friendship(transaction, person1_name, person2_name):
        query = (
            "create (p1:Person { name: $person1_name }) "
            "create (p2:Person { name: $person2_name }) "
            "create (p1)-[:KNOWS]->(p2) "
            "return p1, p2"
        )
        result = transaction.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise exception

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print(f"Found person: {row}")

    @staticmethod
    def _find_and_return_person(transaction, person_name):
        query = """match (p:Person)
        where p.name = $person_name
        return p.name as name"""

        result = transaction.run(query, person_name=person_name)
        return [row["name"] for row in result]

    def find_friends(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._find_and_return_friends, person1_name, person2_name
            )
            for row in result:
                print(f"Found friends: {', '.join(row)}")

            return result

    @staticmethod
    def _find_and_return_friends(transaction, person1_name, person2_name):
        query = (
            "match (p1:Person)-[:KNOWS]->(p2:Person)"
            "where p1.name = $person1_name and p2.name = $person2_name "
            "return p1.name, p2.name"
        )

        result = transaction.run(query, person1_name=person1_name, person2_name=person2_name)
        return [row for row in result]

    def remove_friends(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            result = session.write_transaction(
                self._find_and_remove_friends, person1_name, person2_name
            )
            if result:
                print(f"Removed friends {person1_name} and {person2_name}")
            else:
                print(f"Couldn't remove friends {person1_name} and {person2_name}")

    @staticmethod
    def _find_and_remove_friends(transaction, person1_name, person2_name):
        query = (
            "match (p1:Person)-[:KNOWS]->(p2:Person) "
            "where p1.name = $person1_name and p2.name = $person2_name "
            "detach delete p1, p2"
        )

        try:
            transaction.run(query, person1_name=person1_name, person2_name=person2_name)
            return True
        except TransactionError:
            return False


if __name__ == "__main__":

    # Initializing the app
    app = App(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD)

    # Performing example operations to ensure the connection to Neo4j db
    # as well as the Python driver are working
    ALICE = "Alice"
    DAVID = "David"
    friends_found = app.find_friends(ALICE, DAVID)
    if len(friends_found) > 0:
        app.remove_friends(ALICE, DAVID)

    app.create_friendship(ALICE, DAVID)
    app.find_person(ALICE)
    app.close()
