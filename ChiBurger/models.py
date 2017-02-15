# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_adminstration = db.Column(db.Boolean,default=False)
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def vertify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


# callback function for flask-login extension
# it will load user from session
@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


# category of a post
class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category',  lazy='dynamic')

    # 初始化category的值
    @staticmethod
    def category_init():
        category = Category(name='default')
        db.session.add(category)
        db.session.commit()

    def  __repr__(self):
        return '<Category %r>' % self.name


# comment of an article or a message
class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_ip = db.Column(db.String(20))
    user_platform = db.Column(db.String(15))
    user_browser = db.Column(db.String(20))
    # message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))

    def __repr__(self):
        return '<Comment %r>' % self.body


# an article
class Article(db.Model):

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    body = db.Column(db.Text)
    body_md = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    mod_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', lazy='dynamic')
    like_num = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Article %r>' % self.title


class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    mod_time = db.Column(db.DateTime, default=datetime.utcnow)
    # comments = db.relationship('Comment', lazy='dynamic')

    def __repr__(self):
        return 'Message %r' % self.body
