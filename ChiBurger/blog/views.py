# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from . import blog
from .. import db
from ..models import Article, User, Category
from .forms import ArticleForm

"""
 // TODO: 修改methods和视图对应的html
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
        flash('You have posted successfully!')
    articles = Article.query.all()
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