from flask import jsonify, make_response

from . import db
from .models import User, Article, Comment, Category
from .utils import get_model_columns, get_json_model


def getArticles():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    if articles:
        data = []
        for article in articles:
            dicts = get_model_columns(article)
            comments = article.comments.all()
            if comments:
                comments = get_json_model(comments)
                dicts['comments'] = comments
            else:
                dicts['comments'] = "This article has no comments."
            data.append(dicts)
        return data
        # return jsonify(data)
    # return jsonify({'message':"There's no article right now!"})
    return {'message':"There's no article right now!"}


def getArticle(id):
    article = Article.query.get_or_404(id)
    dicts = get_model_columns(article)
    comments = article.comments.all()
    if comments:
        comments = get_json_model(comments)
        dicts['comments'] = comments
    else:
        dicts['comments'] = "This article has no comments."
    return jsonify(dicts)


def getCategories():
    categories = Category.query.all()
    if categories:
        data = []
        for category in categories:
            dicts = get_model_columns(category)
            articles = category.articles.all()
            if articles:
                articles = get_json_model(articles)
                dicts['articles'] = articles
            else:
                dicts['articles'] = "This category has no articles."
            data.append(dicts)
        return jsonify(data)
    return jsonify({'message':"There's no category right now!"})


def getCategory(id):
    category = Category.query.get_or_404(id)
    dicts = get_model_columns(category)
    articles = category.articles.all()
    if articles:
        articles = get_json_model(articles)
        dicts['articles'] = articles
    else:
        dicts['articles'] = "This category has no articles"
    return jsonify(dicts)


# @api.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


# @api.errorhandler(500)
# def server_error(error):
#     return make_response(jsonify({'error': 'Server error'}), 500)
