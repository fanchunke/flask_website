# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from . import blog
from .. import db
from ..models import Article, User
from .forms import LoginForm, SignupForm

@blog.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    return render_template('blog/index.html', articles=articles)


@blog.route('/<catname>')
def get_category(catname):
    category = Category.query.filter_by(name=catname).first()
    if category is not None:
        articles = category.articles.all()
        return render_template('blog/category.html', articles=articles)
    return redirect(url_for('blog.index'))