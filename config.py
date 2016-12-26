# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}
    
