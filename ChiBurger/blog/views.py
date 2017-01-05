# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import blog
from .. import db, moment
from ..models import Article, User, Category
from ..utils import get_json_articleInfo, add_category
from .forms import ArticleForm


@blog.route('/', methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('blog/index.html', articles=articles)

# 返回所有的文章分类
@blog.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('blog/categories.html', categories=categories)

# 返回某一类文章分类
@blog.route('/categories/<name>')
def category(name):
    category = Category.query.filter_by(name=name).first_or_404()
    articles = category.articles.all()
    return render_template('blog/category.html', category=category, articles=articles)

@blog.route('/articles')
def articles():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('blog/articles.html', articles=articles)

# 返回某一篇文章的详情页
@blog.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('blog/article.html', article=article)

# 404错误处理
@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@blog.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

