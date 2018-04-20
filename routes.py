# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import random
import time

from utils import log
from model.User import User
from model.Message import Message
from model.Session import Session


def template(name):
    """
    调用文件名为name的html文件响应对应请求
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_header(headers):
    header = 'HTTP/1.1 200 OK\r\n'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def current_user(request):
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return '【游客】'
    else:
        s = Session.find_by(session_id=session_id)
        expired_time = s.expired_time
        now = time.time()
        if expired_time > now:
            return s.username
        else:
            return '【游客】'


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
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    """
    登陆路由，登陆验证成功后发送 set-cookie 字段及随机生成的 session_id
    """
    # 仅添加content-type字段
    headers = {
        'Content-Type': 'text/html'
    }
    log('login headers', request.headers)
    log('login cookies', request.cookies)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 向headers中添加set-cookie字段
            # 通过设置一个随机字符串生成session_id
            session_id = random_str()
            form = dict(
                session_id=session_id,
                username=u.username
            )
            s = Session.new(form)
            s.save()
            headers['Set-Cookie'] = 'session_id={}'.format(
                session_id
            )
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    username = current_user(request)
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_header(headers)
    r = '{}\r\n{}'.format(header, body)
    log('login 的响应', r)
    return r.encode()


def route_register(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode()


def route_message(request):
    username = current_user(request)
    if username == '【游客】':
        return error(302)
    else:
        log('本次请求的 method', request.method)
        data = request.query
        if len(data) > 0:
            msg = Message.new(data)
            msg.save()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('message.html')
        # 处理msg便于输出
        ms = '<br>'.join([str(m) for m in Message.all()])
        body = body.replace('{{messages}}', ms)
        r = header + '\r\n' + body
        return r.encode()


def route_message_add(request):
    username = current_user(request)
    if username == '【游客】':
        return error()
    else:
        log('本次请求的 method', request.method)
        data = request.form()
        if len(data) > 0:
            msg = Message.new(data)
            msg.save()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('message.html')
        ms = '<br>'.join([str(m) for m in Message.all()])
        body = body.replace('{{messages}}', ms)
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


def route_profile(request):
    username = current_user(request)
    if username == '【游客】':
        return error(code=302)
    else:
        us = User.find_by(username=username)
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('profile.html')
        body = body.replace('{{id}}', str(getattr(us, 'id')))
        body = body.replace('{{username}}', username)
        body = body.replace('{{note}}', getattr(us, 'note'))
        r = header + '\r\n' + body
        return r.encode()


def route_dict():
    """
    路由字典，用于注册分发路由
    """
    d = {
        '/': route_index,
        '/login': route_login,
        '/register': route_register,
        '/messages': route_message,
        '/messages/add': route_message_add,
        '/profile': route_profile,
    }
    return d


def error(code=404):
    e = {
        302: b'HTTP/1.x 302 REDIRECT\r\nLocation: http://localhost:3000/login\r\n',
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')
