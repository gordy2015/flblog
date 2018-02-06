from flask import Flask,render_template,request,session,flash,abort,redirect,url_for
import config
import logging,json,os
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag,User
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from fladmin import MyView, CKTextAreaField,ArtView,LoginForm
from ext import strcut
from flask_session import Session
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_login import LoginManager,login_user,logout_user,login_required



app = Flask(__name__)
app.config.from_object(config)
# app.config['SECRET_KEY'] = '123456'
db.init_app(app)

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='flblog.log',
#                     filemode='w')

app.jinja_env.filters['afilter'] = strcut

admin = Admin(app,name='后台管理系统', template_mode='bootstrap2')

dbs = [Article,Label,Art_Tag]
# admin.add_view(ArtView(Article,db.session,name=u'文章'))
for i in dbs:
    # admin.add_view(ModelView(i,db.session,category='Models')) #TextAera
    admin.add_view(ArtView(i, db.session,category='Models'))
admin.add_view(MyView(name='hello'))
path = op.join(op.dirname(__file__),'static')
admin.add_view(FileAdmin(path,'/static/',name='静态文件'))

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Pls login to access this page"
login_manager.login_message_category = "info"
login_manager.init_app(app)

@app.route('/')
@login_required
def index():
    if request.method == 'GET':
        art = Article.query.filter().all()
        for i in art:
            print(i.title)
    return render_template('index.html', art=art)

@app.route('/article/<string:art_id>')
def article(art_id):
    art = Article.query.get_or_404(art_id)
    t = art.title
    c = art.content
    print(type(art),art,t,c)
    return render_template('article.html', article_one=art)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    # print(form)
    # print(form.data, form.validate_on_submit())
    if request.method == 'POST':
        if form.validate_on_submit():
            u = form.username.data
            p = form.password.data
            user = User.query.filter(User.username==u,User.password==p)
            # user = User.query.filter_by(username=u,password=p)
            try:
                user = user.one()
                login_user(user)
                flash('Logged in successfully')
                # next = request.args.get('next')
                # if not is_safe_url(next):
                #     return abort(400)
                # return redirect(next or url_for('index'))
                return redirect('/admin')
            except Exception as e:
                login_false = 'Username or Password Error, Pls try again'
                return render_template('admin/login.html',form=form,login_false=login_false)
    return render_template('admin/login.html', form=form)


if __name__ == '__main__':
    app.run()
