# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, request, jsonify
from flask_login import login_user, logout_user, login_required, user_login_confirmed

from . import profile
from .. import db

from ..models import User, Article, Profile


@profile.route('/')
def index():
    return render_template('profile/home.html')

@profile.route('/<username>')
def home(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile
    return render_template('profile/index.html', user=user, profile=profile)


@profile.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editProfile(user_id):
    user = User.query.get_or_404(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        request_items = request.values.keys()
        # 如果对象不存在，先创建一个模型实例
        if not profile:
            profile = Profile(user_id=user_id)
        # 在模型字段中遍历请求中出现的字段，并且对其赋值
        # 只对修改的字段进行更新，其余未修改的字段不更新
        for item in request_items:
            request_value = request.values.get(item)
            setattr(profile, item, request_value)
            json_data = {}
            json_data[item] = getattr(profile, item)
        # 将修改后的对象存储到数据库
        db.session.add(profile)
        db.session.commit()
        # 如果是POST提交，最后返回JSON数据，交给前端处理
        return jsonify(json_data)
    return render_template('profile/edit_profile.html', user=user,profile=profile)


# 404错误处理
@profile.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@profile.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500