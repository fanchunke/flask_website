# -*- coding:utf-8 -*-

from . import blog

@blog.route('/')
def index():
	return "This is blog'index page!"