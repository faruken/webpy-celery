"""

    webpy.celery
    ~~~~~~~~~~~~

    Celery wrapper for web.py.

    :copyright: (c) 2011 Faruk Akgul <me@akgul.org>
    :license: BSD, see LICENSE for more details.

"""

import imp
from celery.app import App
from celery.loaders.default import Loader
from celery.utils import get_full_cls_name


class WebLoader(Loader):
    """The loader for the web.py app.
    """

    def read_configuration(self):
        """Read config from :file:`celeryconfig.py` and configure Celery.
        """
        config = self.app.config
        self.configured = True
        return self.setup_settings(config)


class WebCelery(App):
    """Celery wrapper for web.py app.
    """

    loader_cls = get_full_cls_name(WebLoader)

    def __init__(self, app, *args, **kwargs):
        """Initialize the WebCelery.

        ``app``
            The web.py application.

        ``kwargs``
            Keyword arguments. `config` argument must be passed which contains
            the celery configuration.
        """
        self.app = app
        self._config = kwargs.pop('config', None)
        super(WebCelery, self).__init__(app, *args, **kwargs)

    @property
    def config(self):
        """Setup the configuration variables and pass them to loader.
        """
        return WebCelery.import_module(self._config)

    @classmethod
    def import_module(cls, filename, config_module='celeryconfig'):
        """The celery config file is imported and executed and passed to dict.
        """
        module = imp.new_module(config_module)
        module.__file__ = filename
        execfile(filename, module.__dict__)
        return WebCelery.config_to_dict(module)

    @classmethod
    def config_to_dict(cls, module):
        """Puts configuration constant variables to dict.
        """
        mapp = {}
        for key in dir(module):
            mapp[key] = getattr(module, key)
        return mapp
