# -*- coding:utf-8 -*-

import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager

from ChiBurger import create_app, db

# create app instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def make_shell_context():
    return dict(app=app, db=db)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
