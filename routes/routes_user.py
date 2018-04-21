# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model.Session import Session
from model.User import User
from routes.routes_index import (
	random_str,
	current_user,
	http_response,
)
from utils import template


def user_login(request):
	# header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
	# 仅添加content-type字段
	session = None
	if request.method == 'POST':
		form = request.form()
		username = form.get('username')
		password = form.get('password')
		if User.validate_login(username, password):
			u = User.find_by(username=username)
			# 向headers中添加set-cookie字段
			# 通过设置一个随机字符串生成session_id
			session_id = random_str()
			form = dict(
				session_id=session_id,
				user_id=u.id,
			)
			s = Session.new(form)
			s.save()
			session = {'Set-Cookie': 'session_id={}'.format(
				session_id
			)}
			result = '登录成功'
		else:
			result = '用户名或者密码错误'
			u = User.guest()
	else:
		result = ''
		u = current_user(request)

	body = template(
		'login.html',
		username=u.username,
		result=result
	)
	return http_response(body, session)


def user_register(request, all_user=''):
	if request.method == 'POST':
		form = request.form()
		u = User.new(form)
		if u.validate_register():
			result = '注册成功<br>'
			all_user = User.all()
		else:
			result = '用户名或者密码长度必须大于2'
	else:
		result = ''
	body = template('register.html', result=result, all_user=all_user)
	return http_response(body)


def user_profile(request):
	us = User.find_by(username=current_user(request).username)
	body = template(
		'profile.html',
		id=str(getattr(us, 'id')),
		username=current_user(request).username,
		note=current_user(request).username
	)
	return http_response(body)
