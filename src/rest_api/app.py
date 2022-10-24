from flask_cors import CORS

from . import create_app

app = create_app()

cors = CORS(app, resources={r"/stops": {"origins": "*"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
