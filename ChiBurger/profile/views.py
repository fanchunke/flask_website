# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, request, jsonify
from flask_login import login_user, logout_user, login_required, user_login_confirmed, current_user
from flask_uploads import UploadNotAllowed

from . import profile
from .. import db, photos

from ..models import User, Article, Profile, Photo, Message
from ..utils import upload


@profile.route('/')
def index():
    return render_template('profile/home.html')

@profile.route('/<username>')
def home(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile
    messages_num = user.messages.count()
    page = request.args.get('page', 1, type=int)
    pagination = user.messages.order_by(Message.pub_time.desc()).paginate(page, per_page=10, error_out=False)
    messages = pagination.items
    return render_template('profile/index.html', user=user, profile=profile,
                            messages=messages, messages_num=messages_num, pagination=pagination)


@profile.route('/<username>/profile-detail')
def getProfile(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile
    if profile:
        profile = profile.to_json()
        return jsonify(status='success', profile=profile)
    return jsonify(status='fail', error="There's no profile for current user.")


@profile.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def editProfile(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        if not profile:
            profile = Profile(user_id=user.id)

        # form表单提交
        # form = request.form
        # profile.nickname = form.get('nickname')
        # profile.gender = form.get('gender')
        # profile.address = form.get('address')
        # profile.discription = form.get('discription')

        # 前端Ajax提交
        request_items = request.values.keys()
        # 在模型字段中遍历请求中出现的字段，并且对其赋值
        # 只对修改的字段进行更新，其余未修改的字段不更新
        json_data = {}
        for item in request_items:
            request_value = request.values.get(item)
            setattr(profile, item, request_value)
            json_data[item] = getattr(profile, item)
        db.session.add(profile)
        db.session.commit()
        return jsonify(status='success', data=json_data)
    return render_template('profile/edit_profile.html', user=user, profile=profile)


@profile.route('/upload/avatar', methods=['POST'])
@login_required
def uploadAvatar():
    if request.method == 'POST' and 'photo' in request.files:
        photos = current_user.photos
        if photos is None or photos.filter_by(category='avatar').first() is None:
            avatar = Photo(category='avatar', user_id=current_user.id)
        else:
            avatar = photos.filter_by(category='avatar').first()
        url = upload(request.files['photo'])
        avatar.url = url
        current_user.avatar = url
        db.session.add(avatar)
        db.session.add(current_user)
        db.session.commit()

        return jsonify(status='success', url=url)
    return jsonify(status='fail')


@profile.route('/upload/cover', methods=['POST'])
@login_required
def uploadCover():
    profile = current_user.profile
    if profile is None:
        profile = Profile(user_id=current_user.id)
    if request.method == 'POST' and 'photo' in request.files:
        photos = current_user.photos
        if photos is None or photos.filter_by(category='cover').first() is None:
            cover = Photo(category='cover', user_id=current_user.id)
        else:
            cover = photos.filter_by(category='cover').first()
        url = upload(request.files['photo'])
        cover.url = url
        profile.cover = url
        db.session.add(cover)
        db.session.add(profile)
        db.session.commit()

        return jsonify(status='success', url=url)
    return jsonify(status='fail')


@profile.route('/<username>/add-activity', methods=['POST'])
@login_required
def addActivity(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile
    if request.method == 'POST':
        form = request.form
        body = form.get('body')
        message = Message(body=body,user_id=user.id)
        db.session.add(message)
        db.session.commit()
        return jsonify(status='success', message=message.to_json(),
                        user=user.to_json(), profile=profile.to_json())
    return jsonify(status='fail')


# 404错误处理
@profile.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@profile.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500