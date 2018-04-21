# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import random
import time

from model.Session import Session
from model.User import User
from utils import template


def random_str():
	"""
	生成随机字符串
	"""
	seed = 'qphSgn1cir7Fhh5imWsb4doD95jf0cdSsc'
	s = ''
	for i in range(16):
		random_index = random.randint(0, len(seed) - 2)
		s += seed[random_index]
	return s


def route_index(request):
	header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
	body = template('index.html', username=current_user(request).username)
	r = header + '\r\n' + body
	return r.encode()


def route_static(request):
	"""
	根据对应的GET请求，返回相应的图片
	"""
	filename = request.query.get('file', 'doge.gif')
	path = 'static/' + filename
	try:
		with open(path, 'rb') as f:
			header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
			r = header + b'\r\n' + f.read()
			return r
	except FileNotFoundError:
		header = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n'
		r = header + b'\r\n' + b'<h1>NOT FOUND</h1>'
		return r


def current_user(request):
	session_id = request.cookies.get('session_id')
	if session_id is not None:
		s = Session.find_by(session_id=session_id)
		expired_time = s.expired_time
		now = time.time()
		if expired_time > now:
			u = User.find_by(id=s.user_id)
			return u
		else:
			return User.guest()
	else:
		return User.guest()


def response_with_header(headers, code=202):
	header = 'HTTP/1.1 {} GUA\r\n'.format(code)
	header += ''.join([
		'{}: {}\r\n'.format(k, v) for k, v in headers.items()
	])
	return header


def http_response(body, session=None):
	"""
	接收 body，返回完整的响应头
	"""
	headers = {
		'Content-Type': 'text/html'
	}
	if session is not None:
		headers.update(session)
	header = response_with_header(headers, 200)
	r = '{}\r\n{}'.format(header, body)
	return r.encode()


def redirect(url):
	"""
	浏览器在收到 302 响应的时候
	会自动在 HTTP header 里面找 Location 字段并获取一个 url
	然后自动请求新的 url
	"""
	headers = {
		'Location': url
	}
	header = response_with_header(headers, 302)
	r = '{}\r\n'.format(header)
	return r.encode()


def error(code=404):
	e = {
		302: b'HTTP/1.x 302 REDIRECT\r\nLocation: /login\r\n',
		404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
	}
	return e.get(code, b'')
