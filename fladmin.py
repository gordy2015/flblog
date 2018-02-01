from flask import Flask,render_template,request
import config
import logging,json
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView


class MyView(BaseView):
    @expose('/')
    def hello(self):
        return self.render('hello.html')


