from app import flask_app


@flask_app.route("/")
def home():
    return {"message": "Hello World!"}


@flask_app.route("/service", methods=["POST"])
def service():
    return {"success": True}


if __name__ == "__main__":
    flask_app.run(debug=True)
