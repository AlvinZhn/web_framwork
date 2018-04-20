# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model import Model


class User(Model):
    """
    用户信息 model，除 Model 中的 C R 功能外，还包含注册以及登陆验证功能
    """
    def __init__(self, form):
        Model.__init__(self, form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
