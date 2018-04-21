import os.path
import time
from jinja2 import (
    FileSystemLoader,
    Environment,
)


def log(*args, **kwargs):
    # time.time() 返回 unix time
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    with open('log.txt', 'a', encoding='UTF-8') as f:
        # 在控制台输出
        print(dt, *args, **kwargs)
        # 在文件中输出
        print(dt, *args, file=f, **kwargs)


def configured_environment():
    # 获取加载模板的目录
    # path = '{}/templates/'.format(os.path.dirname(__file__))
    path = os.path.join(os.path.dirname(__file__), 'templates')

    # 创建一个加载器，让jinja从设置的目录加载模板
    loader = FileSystemLoader(path)

    # 用加载器创建一个环境, 使其读取模板文件
    return Environment(loader=loader)


def template(path, **kwargs):
    """
    调用文件名为name的html文件响应对应请求
    """
    # 调用 get_template() 方法加载模板并返回
    t = env.get_template(path)
    return t.render(**kwargs)


env = configured_environment()
