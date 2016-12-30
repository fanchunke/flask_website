from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from ..models import Article


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='must add a title'), Length(1,64)])
    body = TextField('Body', validators=[DataRequired()])
    submit = SubmitField()