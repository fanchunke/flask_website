# -*- coding:utf-8 -*-

from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, logout_user, login_required

from . import admin
from .. import db
from ..models import Article, Category
from ..utils import get_json_categoryInfo, add_category

# 分类管理
@admin.route('/categories', methods=['GET','POST'])
@login_required
def categoriesManage():
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/managecategories.html', categories=categories)

# 获取分类的JSON数据
@admin.route('/_get_category_info/<int:id>')
@login_required
def get_category_info(id):
    return get_json_categoryInfo(id)

# 使用Ajax修改分类信息
@admin.route('/edit_category_info', methods=['GET','POST'])
@login_required
def editCategoryInfo():

    # 从Ajax发送的请求中获取JSON格式的数据
    data = request.get_json()

    # 将Ajax的数据更新到Article中
    id = data['id']
    category = Category.query.filter_by(id=id).first()
    category.name = data['category']
    db.session.add(category)
    db.session.commit()

    # 对Ajax请求返回一个响应，响应内容为JSON格式的数据
    return get_json_categoryInfo(id)

# 删除分类
@admin.route('/del_category/<int:id>')
@login_required
def delCategory(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"success":"ok"})