
from flask_sqlalchemy import SQLAlchemy
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