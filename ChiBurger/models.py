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
    avatar = db.Column(db.String(64))
    is_adminstration = db.Column(db.Boolean,default=False)
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    profile = db.relationship('Profile', backref='user', uselist=False)
    photos = db.relationship('Photo', backref='user', lazy='dynamic')
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def vertify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar
        }

    def __repr__(self):
        return '<User %r>' % self.username


# callback function for flask-login extension
# it will load user from session
@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


# profile of a user
class Profile(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nickname = db.Column(db.String(10))
    gender = db.Column(db.String(4))
    address = db.Column(db.String(4))
    discription = db.Column(db.Text)
    about = db.Column(db.Text)
    about_md = db.Column(db.Text)
    cover = db.Column(db.String(64))

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'gender': self.gender,
            'address': self.address,
            'discription': self.discription,
            'about': self.about,
            'about_md': self.about_md
        }

    def __repr__(self):
        return '<Profile %r>' % self.nickname


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


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'article_num': self.articles.count()
        }

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

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'pub_time': self.pub_time,
            'article_id': self.article_id,
            'user_ip': self.user_ip,
            'user_platform': self.user_platform,
            'user_browser': self.user_browser
        }

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
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    like_num = db.Column(db.Integer, default=0)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'pub_time': self.pub_time,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'comments_num': self.comments.count(),
            'like_num': self.like_num
        }

    def __repr__(self):
        return '<Article %r>' % self.title


class Photo(db.Model):

    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    category = db.Column(db.String(20))
    pub_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))




class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    # cat = db.Column(db.String(10))
    body = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    mod_time = db.Column(db.DateTime, default=datetime.utcnow)
    # comments = db.relationship('Comment', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'pub_time': self.pub_time,
            'mod_time': self.mod_time,
            'user_id': self.user_id
        }

    def __repr__(self):
        return 'Message %r' % self.body
