# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model.User import User
from routes import (
	http_response,
	redirect,
)
from utils import template


def admin_users(request):
	"""
	增加一个路由 /admin/users
	只有 id 为 1 的用户可以访问这个页面, 其他用户访问会定向到 /login
	这个页面显示了所有的用户 包括 id username password
	"""
	body = template('admin_users.html', user_list=User.all())
	return http_response(body)


def admin_update(request):
	"""
	类似于update函数，处理在 /admin/users 下提交的表单，修改指定用户 id 的密码
	"""
	if request.method == 'POST':
		data = request.form()
		user_id = int(data.get('id', -1))
		if len(data) > 0:
			us = User.find_by(id=user_id)
			us.password = data.get('password')
			us.save()
	return redirect('/admin/users')
