import os
from datetime import datetime
from flask import Flask, request, jsonify, make_response
import models
from util import CustomJSONEncoder, str_random
from models import db, User, Post

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config.from_pyfile('.env')
models.init_db(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']


def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()


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
    user = User.login(login_id, password)
    if not user:
        return make_response(jsonify(message="Authorization failed."), 400)
    return jsonify(user.as_dict())


@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = [p.as_dict() for p in Post.all()]
    for p in posts:
        p["user"] = User.by_id(p["user_id"]).as_dict()
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def add_posts():
    # バリデーション.
    body = request.form.get("body")
    file = request.files.get("file")
    if not body or not file:
        return make_response(jsonify(message="Some parameters are missing."), 400)
    if not allowed_file(file.filename):
        return make_response(jsonify(message="File type is not allowed."), 400)
    # 画像を保存.
    filename = "u_" + str_random() + "." + get_ext(file.filename)
    file.save(os.path.join('./static/images/photos/', filename))
    # 投稿を保存.
    post = Post()
    post.user_id = request.user.id
    post.image_url = "/static/images/photos/" + filename
    post.body = body
    post.posted_at = datetime.now()
    db.session.add(post)
    db.session.commit()

    return make_response(jsonify(post.as_dict()), 201)


if __name__ == "__main__":
    app.run(debug=True)
