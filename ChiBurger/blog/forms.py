from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='a email is needed'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='must enter a password')])
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='a username is needed.'), Length(1,64)])
    email = StringField('Email',validators=[DataRequired(message='a email is needed'),Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='must enter a password'), EqualTo('confirm', 
        message='Password must match')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def vaidate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')