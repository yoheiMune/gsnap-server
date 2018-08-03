from flask import Flask, request, jsonify, make_response
import models
from models import db, User, Post

app = Flask(__name__)
app.config.from_pyfile('.env')
models.init_db(app)


@app.route("/")
def index():
    return "Hello from flask"


@app.route("/api/login", methods=["POST"])
def login():
    login_id = request.form.get("login_id")
    password = request.form.get("password")
    if not login_id or not password:
        return make_response(jsonify(message="Authorization failed."), 400)
    user = db.session.query(User).filter_by(login_id=login_id, password=password).first()
    if not user:
        return make_response(jsonify(message="Authorization failed."), 400)
    print(user)
    return jsonify(user.as_dict())


if __name__ == "__main__":
    app.run(debug=True)
