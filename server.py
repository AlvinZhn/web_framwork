# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import _thread
import socket
import urllib.parse

from routes import route_dict
from routes import route_static, error
from utils import log


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.raw_data = ''
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.cookies = {}
        self.headers = {}

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


def parsed_path(path):
    # 拆分 path 和 qury
    index = path.find('?')
    if index == -1:
        return path, {}
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
        return path, query


def response_for_path(request):
    request.path, query = parsed_path(request.path)
    request.query = query
    log('path 和 query', request.path, query)
    # 根据 query 请求 生成对应的路由
    r = {
        '/static': route_static,
    }
    r.update(route_dict())
    response = r.get(request.path, error)
    return response(request)


def run(host='0.0.0.0', port=3000):
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
    log('raw data:\n{}\n'.format(r))
    r = r.decode()
    log('request: \n{}\n'.format(r))
    # 处理请求，避免 chrome 空请求
    # 获取path实现路由，获取method和body处理表单
    request = Request()

    # 拆分请求头
    request.raw_data = r
    header, request.body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    parts = h[0].split()
    # 带有query的path
    request.path = parts[1]
    request.methd = parts[0]
    # 为 headers 添加剩余部分
    request.add_headers(h[1:])

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
