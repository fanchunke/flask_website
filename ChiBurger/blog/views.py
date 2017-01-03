# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import blog
from .. import db, moment
from ..models import Article, User, Category
from ..utils import get_json_articleInfo
from .forms import ArticleForm

"""
 // TODO: 修改methods和视图对应的html
 // TODO: 修改flash消息的显示问题
"""
@blog.route('/', methods=['GET', 'POST'])
def index():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          body=form.body.data)
        form.title.data=''
        form.body.data=''
        db.session.add(article)
        db.session.commit()
        flash("You have posted successfully!")
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('blog/index.html', articles=articles, form=form)


@blog.route('/<catname>')
def category(catname):
    category = Category.query.filter_by(name=catname).first()
    if category is not None:
        articles = category.articles.all()
        return render_template('blog/category.html', articles=articles)
    return redirect(url_for('blog.index'))


@blog.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('blog/article.html', article=article)


"""
// TODO: 考虑文章内容增加、修改、更新、删除等的实现方式
// TODO: 是通过增加视图函数还是通过JavaScript
"""

# return json response for an article
@blog.route('/_get_article_info/<int:id>')
@login_required
def get_article_info(id):
    if current_user.is_authenticated:
        return get_json_articleInfo(id)
    return redirect(url_for('main.login'))

# return to a HTML page to manage articles
# user must login in
@blog.route('/articles', methods=['GET','POST'])
@login_required
def articlesManage():
    if current_user.is_authenticated:
        articles = Article.query.all()
        return render_template('blog/managearticles.html', articles=articles)
    return redirect(url_for('main.login'))

"""
// TODO 修改文章信息后的表单更新，并存储在数据库中
"""
@blog.route('/edit_article_info', methods=['GET','POST'])
@login_required
def editArticleInfo():

    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    # 从Ajax发送的请求中获取JSON格式的数据
    data = request.get_json()

    # 从数据中获取文章分类，如果该分类在数据库中不存在，则创建它
    cat_name = data['category']
    category = Category.query.filter_by(name=cat_name).first()
    if category is None:
        category = Category(name=cat_name)
        db.session.add(category)
        db.session.commit()

    # 将Ajax的数据更新到Article中
    id = data['id']
    article = Article.query.filter_by(id=id).first()
    if article:
        article.title = data['title']
        article.category_id = category.id
        db.session.add(article)
        db.session.commit()

    # 对Ajax请求返回一个响应，响应内容为JSON格式的数据
    return get_json_articleInfo(id)


@blog.route('/del_article/<int:id>')
@login_required
def delArticle(id):
    
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    return jsonify({"success":"ok"})