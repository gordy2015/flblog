from flask import Flask,render_template,request
import config
import logging,json
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from wtforms import (widgets,StringField,TextAreaField,TextField,PasswordField,BooleanField,ValidationError)
from flask_admin.contrib.fileadmin import FileAdmin


class MyView(BaseView):
    @expose('/')
    def hello(self):
        return self.render('admin/hello.html')

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class','ckeditor')
        return super(CKTextAreaWidget,self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

# class ArtView(MyView):
#     form_overrides = dict(content=CKTextAreaField)
#     # column_searchable_list = ('content','title')
#     # column_filters = ('id',)
#     create_template = 'admin/art_edit.html'
#     edit_template = 'admin/art_edit.html'

class ArtView(ModelView):
    extra_js = ["//cdn.ckeditor.com/4.8.0/standard/ckeditor.js"]
    form_overrides = {'content': CKTextAreaField}




