# -*- coding:utf-8 -*-

from flask import Flask
from config import config

def create_app(config_name):
    # initialize app
    app = Flask(__name__, instance_relative_config=True)
    # import config
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    return app
