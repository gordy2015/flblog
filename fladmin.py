from flask import Flask,render_template,request,flash
import config
import logging,json
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag,User
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from wtforms import (widgets,StringField,TextAreaField,TextField,PasswordField,BooleanField,ValidationError)
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms.validators import DataRequired,Length,EqualTo,URL
from flask_wtf import Form,FlaskForm
from flask_login import login_required


class MyView(BaseView):
    @expose('/')
    @login_required
    def hello(self):
        return self.render('admin/hello.html')
    @expose('/a')
    @login_required
    def home(self):
        return self.render('index.html')

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


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(),Length(max=255)])
    password = PasswordField('Password',[DataRequired()])
    remember = BooleanField('Remember Me')
    def validate(self):
        check_validata = super(LoginForm, self).validate()
        if not check_validata:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username')
            # print(self.username.errors)
            flash(self.username.errors)
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            flash(self.password.errors)
            return False
        return True

