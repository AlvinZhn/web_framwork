# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model import Model


class Message(Model):
    """
    一个简单的信息存储 model，将前端发送的消息储存在数据文件中
    """

    def __init__(self, form):
        super().__init__(form)
        self.author = form.get('author', '')
        self.message = form.get('message', '')
