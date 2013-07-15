"""
Janitor
=======

Janitor is a simple HTTP Server that supports OAuth authentication.
"""
from setuptools import find_packages, setup


setup(
    name='Janitor',
    version='0.0.1',
    url='https://github.com/kimjayd/janitor',
    license='MIT License',
    author='Hyunjun Kim',
    author_email='kim@hyunjun.kr',
    description='Simple HTTP Server behind the OAuth',
    long_description=__doc__,
    packages=find_packages(),
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
