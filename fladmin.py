from flask import Flask,render_template,request,flash,redirect,url_for
import config
import logging,json
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag,User
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import (widgets,StringField,TextAreaField,TextField,PasswordField,BooleanField,ValidationError)
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms.validators import DataRequired,Length,EqualTo,URL
from flask_wtf import Form,FlaskForm
from flask_login import login_required,current_user


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
    extra_js = ["/static/ckeditor/ckeditor.js"]
    form_overrides = {'content': CKTextAreaField}
    def is_accessible(self):
        return current_user.is_authenticated
    #实现没登陆时跳转至登陆页面
    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for('login', next=request.url))
        return redirect(url_for('login'))


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


class MyView(BaseView):
    # def is_accessible(self):
    #     if current_user.is_authenticated:
    #         return True
    #     return False
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    @expose('/')
    def index(self):
        # return self.render('admin/hello.html')
        return redirect('/')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    #实现没登陆时跳转至登陆页面
    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for('login', next=request.url))
        return redirect(url_for('login'))
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated
    #实现没登陆时跳转至登陆页面
    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for('login', next=request.url))
        return redirect(url_for('login'))