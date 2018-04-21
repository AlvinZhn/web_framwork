# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model.Message import Message
from routes.routes_index import http_response
from utils import log, template


def messages_index(request):
	log('本次请求的 method', request.method)
	data = request.query
	if len(data) > 0:
		Message.new(data)
	# 处理msg便于输出
	body = template('message.html', messages=Message.all())
	return http_response(body)


def messages_add(request):
	log('本次请求的 method', request.method)
	data = request.form()
	if len(data) > 0:
		Message.new(data)
	body = template('message.html', messages=Message.all())
	return http_response(body)
