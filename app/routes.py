from app import app


@app.route("/")
def home():
    return {"message": "Hello World!"}


@app.route("/service", methods=["POST"])
def service():
    return {"success": True}
