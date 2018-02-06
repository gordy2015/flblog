from flask import Flask,render_template,request
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


class MyView(BaseView):
    @expose('/')
    def hello(self):
        return self.render('admin/hello.html')
    @expose('/a')
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
    # def validate(self):
    #     check_validata = super(LoginForm, self).validate()
    #     if not check_validata:
    #         return False
    #     user = User.query.filter_by(username=self.username.data).first()
    #     if not user:
    #         self.username.errors.append('Invalid username or password')
    #         return False
    #     if not user.check_password(self.password.data):
    #         self.password.errors.append('Invalid username or password')
    #         return False
    #     return True


# from urllib.request import urlparse,urljoin
# from flask import request,url_for
# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url,target))
#     return test_url.scheme in ('http','https') and ref_url.netloc = test_url.netloc
