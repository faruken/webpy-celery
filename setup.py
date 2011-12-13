"""

web.py-celery

"""

from setuptools import (setup, find_packages)
from webpy_celery import (__version__, __doc__)

setup(

    name='webpy-celery',
    version=__version__,
    url='',
    url='http://github.com/faruken/webpy-celery',
    license='BSD',
    author='Faruk Akgul',
    author_email='me@akgul.org',
    description='Celery wrapper for web.py framework',
    long_description=__doc__,
    zip_safe=False,
    packages=find_packages(exclude=['examples', 'tests']),
    platforms='any',
    install_requires=[
        'web.py>=0.34',
        'celery>=2.3.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
