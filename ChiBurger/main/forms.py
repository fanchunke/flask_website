# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(message='a email is needed'), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(message='must enter a password')])
    submit = SubmitField(u'登录')


class SignupForm(FlaskForm):
    username = StringField(u'用户名',validators=[DataRequired(message='a username is needed.'), Length(1,64)])
    email = StringField(u'邮箱',validators=[DataRequired(message='a email is needed'),Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(message='must enter a password'), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def vaidate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')