# -*- coding:utf-8 -*-

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import config

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'blog.login'
bootstrap = Bootstrap()

def create_app(config_name):
    # initialize app
    app = Flask(__name__, instance_relative_config=True)

    # import config
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    # flask extensions initial
    db.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # import blueprint
    from .admin import admin as admin_blueprint
    from .blog import blog as blog_blueprint

    # register blueprint
    app.register_blueprint(admin_blueprint,url_prefix='/admin')
    app.register_blueprint(blog_blueprint)

    return app
