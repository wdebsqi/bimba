import os

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") if os.getenv("NEO4J_PASSWORD") else ""
NEO4J_URL = os.getenv("NEO4J_URL") if os.getenv("NEO4J_URL") else ""
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") if os.getenv("NEO4J_USERNAME") else ""
