import os
from datetime import datetime
from flask import Flask, request, jsonify, make_response
import models
from util import CustomJSONEncoder, str_random
from models import db, User, Post, PostLike, PostComment
from sqlalchemy import desc

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
    if request.path == "/api/login" or request.path.startswith("/static"):
        return None
    api_token = request.args.get('api_token')
    user = User.from_api_key(api_token)
    if not user:
        return make_response(jsonify({"message": "Not Authorized."}), 401)
    request.user = user


@app.route("/api/login", methods=["POST"])
def login():
    login_id = request.json.get("login_id")
    password = request.json.get("password")
    print("login:", login_id, password)
    user = User.login(login_id, password)
    if not user:
        return make_response(jsonify(message="Authorization failed."), 400)
    return jsonify(user.as_dict())


@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = [p.as_dict() for p in Post.query.order_by(desc(Post.id)).all()]
    for p in posts:
        p["user"] = User.by_id(p["user_id"]).as_dict()
        like_users = PostLike.user_ids(p["id"])
        p["num_of_likes"] =  len(like_users)
        p["liked"] = (request.user.id in like_users)
        p["num_of_comments"] = len(PostComment.comments(p["id"]))
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


@app.route("/api/posts/<path:post_id>/likes", methods=["POST"])
def add_like(post_id):
    post = Post.by_id(post_id)
    if not post:
        return make_response(jsonify({"message" : "Not Found."}), 404)
    post_like = PostLike.user_like(post_id, request.user.id)
    if post_like:
        return make_response(jsonify({"message": "Already liked."}), 400)
    post_like = PostLike()
    post_like.post_id = post_id
    post_like.user_id = request.user.id
    db.session.add(post_like)
    db.session.commit()
    return make_response(jsonify(post_like.as_dict()), 201)


@app.route("/api/posts/<path:post_id>/likes", methods=["DELETE"])
def remove_like(post_id):
    post = Post.by_id(post_id)
    if not post:
        return make_response(jsonify({"message" : "Not Found."}), 404)
    post_like = PostLike.user_like(post_id, request.user.id)
    if not post_like:
        return make_response(jsonify({"message": "Liked post not found."}), 400)
    db.session.delete(post_like)
    db.session.commit()
    return make_response(jsonify({"message": "Deleted."}), 200)


@app.route("/api/posts/<path:post_id>/comments", methods=["GET"])
def get_comment(post_id):
    comments = [c.as_dict() for c in PostComment.comments(post_id)]
    for c in comments:
        c["user"] = User.by_id(c["user_id"]).as_dict()
    return jsonify(comments)


@app.route("/api/posts/<path:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    # バリデーション.
    comment = request.form.get("comment")
    if not comment:
        return make_response(jsonify({"message": "comment must be set."}), 400)
    post = Post.by_id(post_id)
    if not post:
        return make_response(jsonify({"message" : "Not Found."}), 404)
    post_comment = PostComment()
    post_comment.post_id = post_id
    post_comment.user_id = request.user.id
    post_comment.comment = comment
    db.session.add(post_comment)
    db.session.commit()
    post_comment.id  # データにタッチすることで、主キーを取得.
    return make_response(jsonify(post_comment.as_dict()), 201)


@app.route("/api/comments/<path:comment_id>", methods=["DELETE"])
def remove_comment(comment_id):
    post_comment = PostComment.by_id(comment_id)
    if not post_comment:
        return make_response(jsonify({"message" : "Not Found."}), 404)
    if post_comment.user_id != request.user.id:
        return make_response(jsonify({"message" : "Not Found."}), 404)
    db.session.delete(post_comment)
    db.session.commit()
    return make_response(jsonify({"message": "Deleted."}), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
