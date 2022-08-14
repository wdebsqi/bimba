from flask import Flask
from src import neo4j_instance

app = Flask(__name__)


@app.route("/")
def home():
    ping_result = neo4j_instance.ping()
    return {"Neo4j db ping status": ping_result}


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
