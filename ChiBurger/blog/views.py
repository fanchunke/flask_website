# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import blog
from .. import db, moment
from ..models import Article, User, Category
from ..utils import get_json_articleInfo, add_category
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


@blog.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('blog/categories.html', categories=categories)


@blog.route('/categories/<name>')
def category(name):
    category = Category.query.filter_by(name=name).first()
    if category is not None:
        articles = category.articles.all()
        return render_template('blog/category.html', category=category, articles=articles)
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
    return get_json_articleInfo(id)

# return to a HTML page to manage articles
# user must login in
@blog.route('/articles', methods=['GET','POST'])
@login_required
def articlesManage():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('blog/managearticles.html', articles=articles)

"""
// TODO 修改文章信息后的表单更新，并存储在数据库中
"""
@blog.route('/edit_article_info', methods=['GET','POST'])
@login_required
def editArticleInfo():

    # 从Ajax发送的请求中获取JSON格式的数据
    data = request.get_json()

    # 从数据中获取文章分类，如果该分类在数据库中不存在，则创建它
    cat_name = data['category']
    category = add_category(name=cat_name)
    # category = Category.query.filter_by(name=cat_name).first()
    # if category is None:
    #     category = Category(name=cat_name)
    #     db.session.add(category)
    #     db.session.commit()

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
    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    return jsonify({"success":"ok"})


@blog.route('/add_article', methods=['GET', 'POST'])
@login_required
def addArticle():
    if request.method == 'POST':
        if request.form['editormd-html-code']:
            title = request.form['title']
            category_name = request.form['category']
            category = add_category(name=category_name)
            body = request.form['editormd-html-code']
            body_md = request.form['editormd-markdown-doc']
            article = Article(title=title,category_id=category.id,body=body,body_md=body_md)
            db.session.add(article)
            db.session.commit()
        return redirect(url_for('blog.article', id=article.id))
    return render_template('blog/addarticle.html')

@blog.route('/edit_article/<int:id>', methods=['GET','POST'])
@login_required
def editArticle(id):
    article = Article.query.filter_by(id=id).first()
    if request.method == 'POST':
        article.title = request.form['title']
        category_name = request.form['category']
        category = add_category(name=category_name)
        article.category_id = category.id
        article.body = request.form['editormd-html-code']
        article.body_md = request.form['editormd-markdown-doc']
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('blog.article', id=id))
    return render_template('blog/editarticle.html', article=article)