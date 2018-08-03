from flask import Flask, request, jsonify, make_response
import models
from util import CustomJSONEncoder
from models import db, User, Post

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config.from_pyfile('.env')
models.init_db(app)


@app.before_request
def before_filter():
    if request.path == "/api/login":
        return None
    api_token = request.args.get('api_token')
    user = User.from_api_key(api_token)
    if not user:
        return make_response(jsonify({"message": "Not Authorized."}), 401)
    request.user = user


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


@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = [p.as_dict() for p in Post.all()]
    for p in posts:
        p["user"] = User.by_id(p["user_id"]).as_dict()
    return jsonify(posts)


if __name__ == "__main__":
    app.run(debug=True)
