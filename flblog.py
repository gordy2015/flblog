from flask import Flask,render_template,request,session
import config
import logging,json,os
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from fladmin import MyView, CKTextAreaField,ArtView
from ext import strcut
from flask_session import Session
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

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

@app.route('/')
def index():
    if request.method == 'GET':
        art = Article.query.filter().all()
        for i in art:
            print(i.title)
    return render_template('index.html', art=art)

admin = Admin(app,name='后台管理系统', template_mode='bootstrap2')

dbs = [Article,Label,Art_Tag]
# admin.add_view(ArtView(Article,db.session,name=u'文章'))
for i in dbs:
    # admin.add_view(ModelView(i,db.session,category='Models')) #TextAera
    admin.add_view(ArtView(i, db.session,category='Models'))
admin.add_view(MyView(name='hello'))
path = op.join(op.dirname(__file__),'static')
admin.add_view(FileAdmin(path,'/static/',name='静态文件'))

@app.route('/article/<string:art_id>')
def article(art_id):
    art = Article.query.get_or_404(art_id)
    t = art.title
    c = art.content
    print(type(art),art,t,c)
    return render_template('article.html', article_one=art)


if __name__ == '__main__':
    app.run()
