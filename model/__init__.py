# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""

import json

from utils import log


def save(data, path):
    """
    将用户的注册信息(list or dict)写入文件
    """
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    从文件中读取已有的注册用户信息，转化为dict or list
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


# MVC 架构基本的 Model 类，简单实现 CRUD 中的 C 和 R 功能
class Model(object):
    def __init__(self, form):
        # 从json文件中获取id值，没有则为None
        self.id = form.get('id', None)

    # 获取对应子类数据文件路径
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    # 在对应子类下传入表单中的数据新建实例
    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        # 在对应子类下，读取数据库文件，获取所有数据信息
        # 通过对数据文件内的信息逐条遍历，
        # 并调用 new 函数将每个用户的数据作为实例储存在list中
        # 即获取该子类下的所有实例信息
        # 配合__repr__实现打印功能
        """
        path = cls.db_path()
        # list with dict
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        # 获取该类下已有的所有实例(list)
        models = self.all()
        log('models', models)

        # if user id is None, then add a new user
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id + 1
            models.append(self)
        # if user id exist, update user data
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self
                    break

        l = [m.__dict__ for m in models]
        path = self.db_path()
        # 调用 save 函数将数据写入数据文件中
        save(l, path)

    @staticmethod
    def valid_kwargs(model, kwargs):
        for key, value in kwargs.items():
            if value != getattr(model, key):
                return False
        return True

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法：
        u = User.find_by(username='admin')
        返回一个 username 属性为 'admin' 的 User 实例
        如果有多条这样的数据, 返回第一个
        如果没这样的数据, 返回 None
        """
        # kwargs -> dict
        instances = cls.all()
        for model in instances:
            exist = cls.valid_kwargs(model, kwargs)
            if exist:
                return model
        return None

    @classmethod
    def multi_find_by(cls, **kwargs):
        """
        返回同时所满足有检索条件的实例
        """
        instances = cls.all()
        kw_numbers = len(kwargs)
        for el in instances:
            flag = False
            for i in range(kw_numbers):
                key = list(kwargs.keys())[i]
                if getattr(el, key) == kwargs[key]:
                    flag = True
                else:
                    flag = False
            if flag:
                return el
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        返回同时所满足有检索条件的所有实例的列表
        """
        user_list = []

        instances = cls.all()
        kw_numbers = len(kwargs)
        for el in instances:
            flag = False
            for i in range(kw_numbers):
                key = list(kwargs.keys())[i]
                if getattr(el, key) == kwargs[key]:
                    flag = True
                else:
                    flag = False
            if flag:
                user_list.append(el)
        return user_list

    # 赋予实例可以调用的特性，
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
