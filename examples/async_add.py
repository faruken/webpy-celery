# -*- coding: utf-8 -*-

"""

This is a simple webpy - celery integrated application which runs async.

"""

import web
from webpy_celery.webpy_celery import WebCelery


class Index(object):
    """Add two numbers asynchronously.
    """
    def GET(self):
        web.header('Content-Type', 'text/html; charset=UTF-8')
        i = web.input()
        x = int(i.get('x', 16))
        y = int(i.get('y', 14))
        res = add.apply_async((x, y))
        return '<a href="/res/%(tid)s">%(tid)s</a>' % {'tid': res.task_id}


class Task(object):
    """Receive the result of `add` and display it.
    """
    def GET(self, task_id):
        web.header('Content-Type', 'text/html; charset=UTF-8')
        res = add.AsyncResult(task_id).get(timeout=1.0)
        return res

URLS = (
    r'/', 'Index',
    r'/res/(.*)', 'Task',
)

app = web.application(URLS, globals(), autoreload=False)


def absolute(path):
    import os
    PATH = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(PATH, path)

config_file = absolute('celeryconfig.py')
celery = WebCelery(app, config=config_file)


@celery.task(name='async_add.add')
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.run()
