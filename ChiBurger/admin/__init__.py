# -*- coding:utf-8 -*-

from flask import Blueprint

# create blueprint: admin
admin = Blueprint('admin', __name__)

# after admin blueprint created, import views
from . import views