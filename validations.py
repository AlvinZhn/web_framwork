# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model.Todo import Todo
from routes.routes_index import (
    current_user,
    redirect,
)
from utils import log


def login_required(route_function):
    def wrapper(request):
        u = current_user(request)
        if u.id == -1:
            log('非用户登陆')
            return redirect('/login')
        else:
            return route_function(request)

    return wrapper


def current_user_required(route_function):
    def wrapper(request):
        u = current_user(request)
        if request.method == 'POST':
            data = request.form()
            todo_id = int(data.get('id', -1))
        else:
            todo_id = int(request.query.get('id', -1))
        t = Todo.find_by(id=todo_id)
        if u.id != t.user_id:
            return redirect('/login')
        else:
            return route_function(request)

    return wrapper


def admin_required(route_function):
    def wrapper(request):
        # 验证管理员用户登陆
        u = current_user(request)
        if u.role == 1:
            return route_function(request)
        else:
            return redirect('/login')

    return wrapper
