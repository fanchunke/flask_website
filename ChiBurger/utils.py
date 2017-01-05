# -*- coding:utf-8 -*-

from flask import jsonify
from .models import Article, Category
from . import db

"""
These are some useful functions for current app.
"""

# a method to return JSON Data for an article instance
def get_json_articleInfo(id):
    article = Article.query.get_or_404(id)
    if article.category is None:
        article.category_id = Category.query.filter_by(name='default').first().id
        db.session.add(article)
        db.session.commit()
    return jsonify({
                    "id": article.id, 
                    "title": article.title, 
                    "body": article.body,
                    "pub_time": article.pub_time,
                    "mod_time": article.mod_time,
                    "user": article.user, 
                    "category": article.category.name,
                    "comments_num": article.comments.count(),
                    "like_num": article.like_num
                    })


def add_category(name):
    category = Category.query.filter_by(name=name).first()
    if category is None:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
    return category


def get_json_categoryInfo(id):
    category = Category.query.filter_by(id=id).first()
    if category is not None:
        return jsonify({
                        "id": category.id,
                        "name": category.name,
                        "articles_num": category.articles.count()
                        })