# -*- coding:utf-8 -*-

from datetime import datetime
from flask import jsonify, make_response, request
from flask_login import login_required

from . import api
from .. import db
from ..models import User, Article, Comment, Category
from ..utils import add_category


# 查询所有文章
@api.route('/articles')
def getArticles():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    if articles:
        articles = [article.to_json() for article in articles]
        return jsonify(status='success', articles=articles)
    return jsonify(status='fail', error="There's no articles")


# 查询指定id的文章
@api.route('/article/<int:id>')
def getArticle(id):
    article = Article.query.get_or_404(id)
    comments = article.comments.all()
    if comments:
        comments = [comment.to_json() for comment in comments]
        return jsonify(status='success', article=article.to_json(), comments=comments)
    return jsonify(status='success', article=article.to_json(),
                comments="This article has no comments")


# 增加新的文章
@api.route('/article/add', methods=['POST'])
# @login_required
def addArticle():
    form = request.form
    title = form.get('title')
    category_name = form.get('category')
    category = add_category(name=category_name)
    body = form.get('editormd-html-code')
    body_md = form.get('editormd-markdown-doc')
    article = Article(title=title, category_id=category.id,
                        body=body, body_md=body_md)
    db.session.add(article)
    db.session.commit()
    return jsonify(status='success')


# 更新指定id的文章
@api.route('/article/<int:id>/update', methods=['POST'])
# @login_required
def updateArticle(id):
    article = Article.query.get_or_404(id)
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
    return jsonify(status='success')


# 删除指定id的文章
@api.route('/article/<int:id>/delete', methods=['POST'])
# @login_required
def deleteArticle(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify(status='success')


# 查询所有分类信息
@api.route('/categories')
def getCategories():
    categories = Category.query.order_by(Category.id.desc()).all()
    if categories:
        categories=[category.to_json() for category in categories]
        return jsonify(status='success', categories=categories)
    return jsonify(status='fail', error="There's no categories")


# 查询指定id的分类信息
@api.route('/category/<int:id>')
def getCategory(id):
    category = Category.query.get_or_404(id)
    articles = category.articles.all()
    if articles:
        return jsonify(status='success', category=category.to_json(),
                    articles=[article.to_json() for article in articles])
    return jsonify(status='success', category=category.to_json(),
                articles="There's no articles in this category")


# 增加新的分类
@api.route('/category/add', methods=['POST'])
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
@api.route('/category/<int:id>/update', methods=['POST'])
# @login_required
def updateCategory(id):
    category = Category.query.get_or_404(id)
    form = request.form
    category.name = form.get('category-name')
    db.session.add(category)
    db.session.commit()
    return jsonify(status='success')


# 删除指定id的分类
@api.route('/category/<int:id>/delete', methods=['POST'])
# @login_required
def deleteCategory(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(status='success')


# 在指定id的文章中添加评论
@api.route('/article/<int:id>/add-comment', methods=['POST'])
def addComments(id):
    form = request.form
    body = form.get('comment-body')
    article_id = id
    comment = Comment(body=body, article_id=article_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(status='success')


# 删除指定id的评论
@api.route('/comment/<int:id>/delete', methods=['POST'])
# @login_required
def deleteComment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify(status='success')


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify(status='fail', error='Not found'), 404)


@api.errorhandler(500)
def server_error(error):
    return make_response(jsonify(status='fail', error='Server error'), 500)
