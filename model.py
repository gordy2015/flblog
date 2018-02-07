
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
import datetime

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(64), nullable=True)
    tag_id = db.Column(db.Integer)

class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(64))

class Art_Tag(db.Model):
    __tablename__ = 'art_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_id = db.Column(db.Integer)
    lab_id = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    def is_anonymous(self):
        if isinstance(self,AnonymousUserMixin):
            return True
        else:
            return False