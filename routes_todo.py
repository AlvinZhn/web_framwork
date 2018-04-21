# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import time

from model.Todo import Todo
from routes import (
	redirect,
	current_user,
	http_response,
)
from utils import template


def formatted_time(unix_time):
	time_format = '%Y/%m/%d %H:%M:%S'
	return time.strftime(time_format, time.localtime(unix_time))


def todo_index(request):
	body = template(
		'todo_index.html',
		todos=Todo.find_all(user_id=current_user(request).id)
	)
	return http_response(body)


def todo_add(request):
	if request.method == 'POST':
		data = request.form()
		u = current_user(request)
		if len(data) > 0:
			t = Todo.new(data)
			t.user_id = u.id
			t.created_time = formatted_time(int(time.time()))
			t.updated_time = formatted_time(int(time.time()))
			t.save()
	return redirect('/todo')


def todo_delete(request):
	todo_id = int(request.query.get('id'))
	Todo.remove(todo_id)
	return redirect('/todo')


def todo_edit(request):
	todo_id = int(request.query.get('id', -1))
	t = Todo.find_by(id=todo_id)

	body = template(
		'todo_edit.html',
		todo_id=str(t.id),
		todo_title=t.title
	)
	return http_response(body)


def todo_update(request):
	if request.method == 'POST':
		data = request.form()
		todo_id = int(data.get('id', -1))
		if len(data) > 0:
			t = Todo.find_by(id=todo_id)
			t.title = data.get('title')
			t.updated_time = formatted_time(int(time.time()))
			t.save()
	return redirect('/todo')
