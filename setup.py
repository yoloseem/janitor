from __future__ import with_statement

import codecs
from setuptools import setup


def readme():
    with codecs.open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name='Janitor',
    version='0.0.1',
    url='https://github.com/kimjayd/janitor',
    license='MIT License',
    author='Hyunjun Kim',
    author_email='kim@hyunjun.kr',
    description='Simple HTTP Server behind the OAuth',
    long_description=readme(),
    py_modules=['janitor'],
    install_requires=[
        'Flask',
        'gevent',
        'wsgi-oauth2',
    ],
    entry_points={
        'console_scripts': [
            'janitor=janitor:run'
        ],
    },
    zip_safe=False,
    platforms='any',
)
