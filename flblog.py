from flask import Flask,render_template,request,session,flash,abort,redirect,url_for
import config
import logging,json,os
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag,User
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from fladmin import MyView, CKTextAreaField,ArtView,LoginForm,MyAdminIndexView,MyFileAdmin
from ext import strcut
from flask_session import Session
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from ext import bcrypt
from flask_principal import Principal,Permission,identity_loaded,RoleNeed,UserNeed,Identity,AnonymousIdentity,identity_changed,current_app

app = Flask(__name__)
app.config.from_object(config)
# app.config['SECRET_KEY'] = '123456'
db.init_app(app)

bcrypt.init_app(app)

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='flblog.log',
#                     filemode='w')

app.jinja_env.filters['afilter'] = strcut



flask_admin = Admin(app,name='后台管理系统', template_mode='bootstrap3',index_view=MyAdminIndexView())

# admin.add_view(ArtView(Article,db.session,name=u'文章'))
dbs = [Article,Label,Art_Tag]
for i in dbs:
    # admin.add_view(ModelView(i,db.session,category='Models')) #TextAera
    flask_admin.add_view(ArtView(i, db.session,category='数据库操作'))
flask_admin.add_view(MyView(name='查看主页'))
path = op.join(op.dirname(__file__),'static')
flask_admin.add_view(MyFileAdmin(path,'/static/',name='静态文件'))
# flask_admin.init_app(app)


login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Pls login to access this page"
login_manager.login_message_category = "info"
login_manager.init_app(app)


principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
default_permission = Permission(RoleNeed('default'))
principals.init_app(app)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender,identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user,'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page=1):
    if request.method == 'GET':
        art = Article.query.filter().paginate(page, config.POSTS_PER_PAGE, False)
        # for i in art:
        #     print(i.title)
        # print(art.page, art.pages)
        label_detail = Label.query.filter().all()
    return render_template('index.html', art=art,label_detail=label_detail)


@app.route('/article/<string:art_id>')
def article(art_id):
    art = Article.query.get_or_404(art_id)
    # t = art.title
    # c = art.content
    # print(type(art),art,t,c)
    label_detail = Label.query.filter().all()
    return render_template('article.html', article_one=art,label_detail=label_detail)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # return User.query.filter_by(id=user_id).first()

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/admin')
    if request.method == 'POST':
        # print(form.validate_on_submit())
        # print(bcrypt.generate_password_hash(p).decode('utf-8'))
        if form.validate_on_submit():
            u = form.username.data
            p = form.password.data
            # user = User.query.filter(User.username==u,User.password==p)
            user = User.query.filter_by(username=form.username.data).one()
            login_user(user,remember=form.remember.data)
            m = identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))
            # print(u,p,m)
            flash('Logged in successfully')
            # next = request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            # return redirect(next or url_for('index'))
            return redirect('/admin')
    return render_template('admin/login.html', form=form)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
