from flask import Flask,render_template,request
import config
import logging,json
from flask_sqlalchemy import SQLAlchemy
from model import db,Article,Label,Art_Tag
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from fladmin import MyView

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='flblog.log',
#                     filemode='w')


@app.route('/')
def index():
    if request.method == 'GET':
        art = Article.query.filter().all()
        for i in art:
            print(i.title)
    return render_template('index.html', art=art)

admin = Admin(app,name='后台管理系统', template_mode='bootstrap2')
dbs = [Article,Label,Art_Tag]
for i in dbs:
    admin.add_view(ModelView(i, db.session,category='Models'))
admin.add_view(MyView(name='hello'))


if __name__ == '__main__':
    app.run()
