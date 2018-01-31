from flask import Flask
import os, sqlite3
from flask_sqlalchemy import SQLAlchemy

Flask.debug = True
Flask.reload = True
DATABASE = 'flblogdb.sqlite'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
