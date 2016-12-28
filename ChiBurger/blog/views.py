# -*- coding:utf-8 -*-

from flask import render_template, url_for, abort, redirect, flash, request
from flask_login import login_user

from . import blog
from .. import db
from ..models import Article, User
from .forms import LoginForm, SignupForm

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
                return redirect(request.args.get('next') or url_for('blog.index'))
            flash('Invalid password')
        else:
            flash('Invalid email')
    return render_template('blog/login.html',form=form)

@blog.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are registered successfully. Now you can login.')
        return redirect(url_for('blog.login'))
    return render_template('blog/signup.html', form=form)