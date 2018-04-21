# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import _thread
import socket
import urllib.parse

from routes.routes_index import (
	route_index,
	route_static,
	error
)
from routes import (
	routes_user,
	routes_message,
	routes_todo,
	routes_admin,
)
from utils import log
from validations import (
	login_required,
	current_user_required,
	admin_required,
)


# 定义一个 class 用于保存请求的数据
class Request(object):
	def __init__(self, raw_data):
		# 拆分请求头
		header, self.body = raw_data.split('\r\n\r\n', 1)
		h = header.split('\r\n')
		parts = h[0].split()
		self.method = parts[0]
		# 带有query的path
		path = parts[1]
		self.path = ''
		self.query = {}
		# get self.path and self.query from path
		self.parsed_path(path)
		log('Request: path 和 query', self.path, self.query)
		self.cookies = {}
		self.headers = {}
		# 为 headers 添加剩余部分
		self.add_headers(h[1:])

	def add_cookies(self):
		cookies = self.headers.get('Cookie', '')
		kvs = cookies.split('; ')
		log('cookie', kvs)
		for kv in kvs:
			if '=' in kv:
				k, v = kv.split('=')
				self.cookies[k] = v

	def add_headers(self, header):
		# 处理 header 中的数据，取出其余部分
		for line in header:
			k, v = line.split(': ', 1)
			self.headers[k] = v
		# 清空cookie
		self.cookies = {}
		self.add_cookies()

	def form(self):
		# 处理post请求中的body部分
		log('self.body', self.body)
		args = self.body.split('&')
		f = {}
		for arg in args:
			log('form', arg)
			arg = urllib.parse.unquote_plus(arg)
			log('unquote form', arg)
			k, v = arg.split('=')
			f[k] = v
		log('form() 字典', f)
		return f

	def parsed_path(self, path):
		"""
    	拆分 path 和 qury
        """
		index = path.find('?')
		if index == -1:
			self.path = path
			self.query = {}
		else:
			path, query_string = path.split('?', 1)

			args = query_string.split('&')
			query = {}
			if args[0].find('=') != -1:
				for arg in args:
					k, v = arg.split('=')
					query[k] = v
			else:
				query['file'] = query_string
			self.path = path
			self.query = query
		log('path 和 query', self.path, self.query)


def response_for_path(request):
	# 自动进行路由分发
	routes_dict = {
		'/': route_index,
		'/static': route_static,
	}
	routes = [routes_todo, routes_user, routes_admin, routes_message]
	for route in routes:
		# 获取路由函数内所有的函数（路由）名
		names = dir(route)
		route_prefix = route.__name__.split('_')[1]
		function_names = [name for name in names if name.startswith(route_prefix)]
		for name in function_names:
			# 生成对应的路由path
			if name.startswith('user'):
				key = '/{}'.format(name.split('_')[1])
				if 'profile' in name:
					value = login_required(getattr(route, name))
				else:
					value = getattr(route, name)
			elif 'index' in name:
				key = '/{}'.format(name.split('_')[0])
				value = login_required(getattr(route, name))
			else:
				key = '/{}'.format(name.replace('_', '/'))
				if 'messages' in name:
					value = login_required(getattr(route, name))
				elif 'admin' in name:
					value = admin_required(getattr(route, name))
				elif 'add' in name:
					value = login_required(getattr(route, name))
				else:
					value = current_user_required(getattr(route, name))
			# 获取对应路径的路由函数
			routes_dict[key] = value

	response = routes_dict.get(request.path, error)
	return response(request)


def run(host='', port=3000):
	"""
    启动服务器
    """

	# 初始化服务器
	log('开始运行于', '{}:{}'.format(host, port))
	with socket.socket() as s:
		s.bind((host, port))
		s.listen(5)

		# 接收请求
		while True:
			connection, address = s.accept()

			log('ip, {}\n'.format(address))

			_thread.start_new_thread(
				process_request, (connection,)
			)


def process_request(connection):
	r = connection.recv(1024)
	r = r.decode()
	log('request, {}\n'.format(r))
	# 处理请求，避免 chrome 空请求
	# 获取path实现路由，获取method和body处理表单
	request = Request(r)

	# 根据请求，返回对应的处理函数
	response = response_for_path(request)
	connection.sendall(response)

	# 处理完成，断开连接
	connection.close()


if __name__ == '__main__':
	# 生成配置并且运行程序
	config = dict(
		host='0.0.0.0',
		port=3000,
	)
	run(**config)
