# -*- coding:utf-8 -*-

from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from . import main
from .. import db
from ..models import User
from .forms import LoginForm, SignupForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.vertify_password(form.password.data):
                login_user(user)
                flash("You have logined in successfully!")
                return redirect(request.args.get('next') or url_for('blog.index'))
            flash('Invalid password')
        else:
            flash('Invalid email')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("You have signed up successfully. Now you can login in.")
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

