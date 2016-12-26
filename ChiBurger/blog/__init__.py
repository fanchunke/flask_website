# -*- coding:utf-8 -*-

from flask import Blueprint

# create blueprint:blog
blog = Blueprint('blog', __name__)

# after blueprint created, import views
from . import views