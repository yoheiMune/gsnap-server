from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class AbstractModel():
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password"}


class User(AbstractModel, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    api_token = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()

    @classmethod
    def from_api_key(cls, api_token):
        if not api_token:
            return None
        return db.session.query(cls).filter_by(api_token=api_token).first()

    @classmethod
    def login(cls, login_id, password):
        if not login_id or not password:
            return None
        return db.session.query(User).filter_by(login_id=login_id, password=password).first()


class Post(AbstractModel, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255))
    body = db.Column(db.Text())
    posted_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def all(cls):
        return db.session.query(cls)
