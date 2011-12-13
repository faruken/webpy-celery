"""
    Unit Test for webpy-celery.

    :copyright: Faruk Akgul, <me@akgul.org>
    :license: BSD, see LICENSE for details.
"""

import web
from celery.tests.utils import unittest
from webpy_celery.webpy_celery import (WebCelery, WebLoader)


def absolute(path):
    """Get the real path for the :file:`path`. In this case `celeryconfig.py`.
    """
    import os
    abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(abs_path, path)


class TestCelery(unittest.TestCase):
    """Unit test is based on Celery's test cases.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the config file.
        """
        self._config = absolute('celeryconfig.py')
        super(TestCelery, self).__init__(*args, **kwargs)

    def setup(self):
        """Setup a web.py application.
        """
        urls = (r'/', 'index')
        app = web.application(urls, globals())
        return app

    def test_loader_conf(self):
        """Testing the :file:`celeryconfig.py` constants.
        """
        app = self.setup()
        celery = WebCelery(app, config=self._config)
        self.assertEqual(celery.conf.BROKER_TRANSPORT, 'memory')
        self.assertIsInstance(celery.loader, WebLoader)
        self.assertTrue(celery.loader.configured)

    def test_worker(self):
        """Testing the celery workers.
        """
        app = self.setup()
        celery = WebCelery(app, config=self._config)
        worker = celery.Worker()
        self.assertTrue(worker)

    def test_connection(self):
        """Connection test.
        """
        app = self.setup()
        celery = WebCelery(app, config=self._config)
        Task = celery.create_task_cls()
        conn = Task.establish_connection()
        self.assertIn('kombu.transport.memory', repr(conn.create_backend()))
        conn.connect()

    def test_app_async(self):
        """Async tests.
        """
        app = self.setup()
        celery = WebCelery(app, config=self._config)

        @celery.task(name='test.add_async', serializer='msgpack')
        def add(x, y):
            return x + y

        res = add.apply_async((4, 4))
        self.assertTrue(res.task_id)
        self.assertEqual(add.serializer, 'msgpack')

    def test_app_task(self):
        """App task tests.
        """
        app = self.setup()
        celery = WebCelery(app, config=self._config)

        @celery.task(name='test.sub', serializer='json')
        def sub(x, y):
            return x - y

        self.assertEqual(sub(6, 4), 2)
        self.assertEqual(sub.serializer, 'json')
        self.assertTrue(sub.ignore_result)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestCelery))
