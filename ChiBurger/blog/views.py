# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, get_flashed_messages
from flask_login import login_user

from . import blog
from ..models import Article, User
from .forms import LoginForm

@blog.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    return render_template('blog/index.html', articles=articles)

@blog.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.vertify_password(form.password.data):
                login_user(user)
                flash("You were logged in successfully!")

                next = request.get.args('get')
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for('blog.index'))
            flash('Invalid password')
        flash('Invalid email')
    return render_template('blog/login.html',form=form)

