# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import time

from model import Model


class Session(Model):
	def __init__(self, form):
		super().__init__(form)
		self.user_id = form.get('user_id', '')
		self.session_id = form.get('session_id', '')
		self.expired_time = form.get('expired_time', time.time() + 3600)
