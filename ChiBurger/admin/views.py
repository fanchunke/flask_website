# -*- coding:utf-8 -*-

from .articles import *
from .categories import *

@admin.route('/')
def index():
    return render_template('admin/index.html')

# 404错误处理
@admin.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@admin.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500