# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import blog
from .. import db, moment
from ..models import Article, User, Category, Comment
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
    category_num = Category.query.count()
    return render_template('blog/categories.html', 
                            categories=categories,
                            category_num=category_num)

# 返回某一类文章分类
@blog.route('/categories/<name>')
def category(name):
    category = Category.query.filter_by(name=name).first_or_404()
    articles = category.articles.all()
    article_num = category.articles.count()
    return render_template('blog/category.html', 
                            category=category, 
                            articles=articles, 
                            article_num=article_num)

@blog.route('/articles')
def articles():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    article_num = Article.query.count()
    return render_template('blog/articles.html', 
                            articles=articles, 
                            article_num=article_num)

# 返回某一篇文章的详情页
@blog.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    if article:
        comments = article.comments.order_by(Comment.pub_time.desc()).all()
    return render_template('blog/article.html', 
                            article=article, 
                            comments=comments)

# 增加评论
@blog.route('/article/<int:id>/add_comments', methods=['GET', 'POST'])
def addComments(id):
    article = Article.query.get_or_404(id)
    if article:
        comments = article.comments.order_by(Comment.pub_time.desc()).all()
    if request.method == 'POST':
        body = request.form['body']
        user_ip = request.remote_addr
        user_platform = request.user_agent.platform
        user_browser = request.user_agent.browser
        article_id = id
        comment = Comment(body=body, article_id=article_id, user_ip=user_ip,
                            user_platform=user_platform, user_browser=user_browser)
        db.session.add(comment)
        db.session.commit()
        comment_num = article.comments.count()
        return jsonify(id=comment.id,body=comment.body,
                        pub_time=comment.pub_time,
                        article_id=comment.article_id,
                        user_ip=user_ip, 
                        user_platform=user_platform,
                        user_browser=user_browser,
                        comment_num=comment_num)

# 404错误处理
@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@blog.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

