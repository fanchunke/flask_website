# -*- coding:utf-8 -*-

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import config

db = SQLAlchemy()
# toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    # initialize app
    app = Flask(__name__, instance_relative_config=True)

    # import config
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    # flask extensions initial
    db.init_app(app)
    # toolbar.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # import blueprint
    from .admin import admin as admin_blueprint
    from .blog import blog as blog_blueprint
    from .main import main as main_blueprint
    from .profile import profile as profile_blueprint
    from .api import api as api_blueprint

    # register blueprint
    app.register_blueprint(admin_blueprint,url_prefix='/admin')
    app.register_blueprint(blog_blueprint,url_prefix='/blog')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(main_blueprint)

    return app
