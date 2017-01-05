# -*- coding:utf-8 -*-

from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, logout_user, login_required

from . import admin
from .. import db
from ..models import Article, Category
from ..utils import get_json_articleInfo, add_category

# 文章管理
@admin.route('/articles', methods=['GET','POST'])
@login_required
def articlesManage():
    articles = Article.query.order_by(Article.pub_time.desc()).all()
    return render_template('admin/managearticles.html', articles=articles)

# 添加文章
@admin.route('/add_article', methods=['GET', 'POST'])
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
    return render_template('admin/addarticle.html')

# 修改文章
@admin.route('/edit_article/<int:id>', methods=['GET','POST'])
@login_required
def editArticle(id):
    # article = Article.query.filter_by(id=id).first()
    article = Article.query.get_or_404(id)
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
    return render_template('admin/editarticle.html', article=article)

# 删除文章
@admin.route('/del_article/<int:id>')
@login_required
def delArticle(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({"success":"ok"})

# return json response for an article
@admin.route('/_get_article_info/<int:id>')
@login_required
def get_article_info(id):
    return get_json_articleInfo(id)

# 使用Ajax修改文章信息
@admin.route('/edit_article_info', methods=['GET','POST'])
@login_required
def editArticleInfo():

    # 从Ajax发送的请求中获取JSON格式的数据
    data = request.get_json()

    # 从数据中获取文章分类，如果该分类在数据库中不存在，则创建它
    cat_name = data['category']
    category = add_category(name=cat_name)

    # 将Ajax的数据更新到Article中
    id = data['id']
    article = Article.query.get_or_404(id)
    article.title = data['title']
    article.category_id = category.id
    db.session.add(article)
    db.session.commit()

    # 对Ajax请求返回一个响应，响应内容为JSON格式的数据
    return get_json_articleInfo(id)