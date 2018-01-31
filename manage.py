
from flask_script import Manager,Shell
from flask_migrate import MigrateCommand,Migrate
from flblog import app
from model import db,Article,Label,Art_Tag

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()