# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import time

from model import Model


class Session(Model):
    """
    实现 session 本地化和持久化
    """
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.session_id = form.get('session_id', '')
        self.expired_time = form.get('expired_time', time.time() + 3600)

