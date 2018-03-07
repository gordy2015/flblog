from flask import Flask
import os, sqlite3
from flask_sqlalchemy import SQLAlchemy

Flask.debug = True
Flask.reload = True
DATABASE = 'flblogdb.sqlite'
# SESSION_TYPE = 'C:\Users\Administrator\PycharmProjects\filesystem'
# SECRET_KEY= os.urandom(24)
SECRET_KEY = '123456'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# pagination
POSTS_PER_PAGE = 10
