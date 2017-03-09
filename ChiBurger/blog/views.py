# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import blog
from .. import db, moment
from ..models import Article, User, Category, Comment
from .forms import ArticleForm
from ..utils import get_json_articleInfo, add_category


# blog首页展示所有文章
@blog.route('/')
def index():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('blog/index.html', articles=articles)


# 文章归档
@blog.route('/articles')
def articles():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    article_num = Article.query.count()
    return render_template('blog/articles.html', 
                            articles=articles, 
                            article_num=article_num)

# 返回指定id的文章
@blog.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    comments = article.comments.order_by(Comment.pub_time.desc()).all()
    return render_template('blog/article.html', 
                            article=article, 
                            comments=comments)


# 增加新的文章
@blog.route('/article/add', methods=['GET','POST'])
@login_required
def addArticle():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        category_name = form.get('category')
        category = add_category(name=category_name)
        body = form.get('editormd-html-code')
        body_md = form.get('editormd-markdown-doc')
        article = Article(title=title, category_id=category.id,
                            body=body, body_md=body_md, user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('blog.article', id=article.id))
    return render_template('blog/add_article.html')


# 修改指定id的文章
@blog.route('/article/<int:id>/edit', methods=['GET','POST'])
@login_required
def editArticle(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        form = request.form
        article.title = form.get('title')
        category_name = form.get('category')
        category = add_category(name=category_name)
        article.category_id = category.id
        article.body = form.get('editormd-html-code')
        article.body_md = form.get('editormd-markdown-doc')
        article.mod_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('blog.article', id=id))
    return render_template('blog/edit_article.html', article=article)


# 删除指定id的文章
@blog.route('/article/<int:id>/delete')
@login_required
def deleteArticle(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify(status='success')


# 返回所有的文章分类
@blog.route('/categories')
def categories():
    categories = Category.query.all()
    category_num = Category.query.count()
    return render_template('blog/categories.html', 
                            categories=categories,
                            category_num=category_num)

# 返回指定id的文章分类
@blog.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    articles = category.articles.all()
    article_num = category.articles.count()
    return render_template('blog/category.html', 
                            category=category, 
                            articles=articles, 
                            article_num=article_num)


# 增加新的分类
@blog.route('/category/add', methods=['POST'])
# @login_required
def addCategory():
    form = request.form
    name = form.get('category-name')
    category = Category.query.filter_by(name=name).first()
    if category:
        return jsonify(status='fail', error='The category already exists.')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(status='success')


# 更新指定id的分类信息
@blog.route('/category/<int:id>/edit', methods=['POST'])
@login_required
def editCategory(id):
    category = Category.query.get_or_404(id)
    form = request.form
    category.name = form.get('category-name')
    db.session.add(category)
    db.session.commit()
    return jsonify(status='success')


# 删除指定id的分类
@blog.route('/category/<int:id>/delete', methods=['POST'])
@login_required
def deleteCategory(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(status='success')


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

