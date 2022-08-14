import os

from dotenv import load_dotenv

from .Neo4jDB import Neo4jDB

# Loading environment variables from .env file
load_dotenv()
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_instance = Neo4jDB(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD)
