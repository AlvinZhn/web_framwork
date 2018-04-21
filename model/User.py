# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from model import Model


class User(Model):
	def __init__(self, form):
		Model.__init__(self, form)
		self.username = form.get('username', '')
		self.password = form.get('password', '')
		self.note = form.get('note', '')
		self.role = form.get('role', 2)

	@staticmethod
	def validate_login(username, password):
		u = User.find_by(username=username)
		return u is not None and u.password == password

	def validate_register(self):
		return len(self.username) > 2 and len(self.password) > 2

	@staticmethod
	def guest():
		form = dict(
			id=-1,
			username='【游客】',
		)
		u = User.new(form)
		return u
