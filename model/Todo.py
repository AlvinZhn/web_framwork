# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model import Model


class Todo(Model):
	def __init__(self, form):
		super().__init__(form)
		self.title = form.get('title', '')
		self.user_id = form.get('user_id', -1)
		self.created_time = form.get('created_time', 0)
		self.updated_time = form.get('updated_time', 0)
