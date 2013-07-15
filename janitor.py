""" :mod:`janitor`
    ~~~~~~~~~~~~~~

"""
import argparse
import ConfigParser

from flask import Flask, send_from_directory
from gevent.pywsgi import WSGIServer
from werkzeug.contrib.fixers import ProxyFix
from wsgioauth2 import GithubService


class ELBPingPong(object):
    def __init__(self, app, ping='/ping', pong='pong'):
        self.app = app
        self.ping = ping
        self.pong = pong

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if path_info == self.ping:
            start_response('200 OK', [('Content-Type', 'text/plain'),
                                      ('Content-Length', len(self.pong))])
            return self.pong
        return self.app(environ, start_response)


def janitor_factory(options, auth_options):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    @app.route('/<path:path>', methods=['GET'])
    def serve(path=options['default']):
        return send_from_directory(options['base_dir'], path)

    if auth_options['service'].lower() == 'github':
        if 'allowed_orgs' in auth_options:
            service = GithubService(allowed_orgs=auth_options['allowed_orgs'])
        else:
            service = GithubService()
    else:
        raise NotImplementedError()

    client = service.make_client(
        client_id=auth_options['client_id'],
        client_secret=auth_options['client_secret'],
    )

    app.wsgi_app = client.wsgi_middleware(app.wsgi_app,
                                          secret=options['secret_key'])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.wsgi_app = ELBPingPong(app.wsgi_app)
    return app


def run():
    parser = argparse.ArgumentParser(description='Janitor')
    parser.add_argument('-c', '--config', help='configuration file',
                        required=True)
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read(args.config)
    host = config.get('janitor', 'host')
    port = config.getint('janitor', 'port')

    options = {
        'secret_key': config.get('janitor', 'secret_key'),
        'base_dir': config.get('janitor', 'base_dir'),
        'default': 'index.html',
    }
    try:
        default = config.get('janitor', 'default')
    except ConfigParser.NoOptionError:
        pass
    else:
        options['default'] = default

    auth_options = {
        'service': config.get('auth', 'service'),
        'client_id': config.get('auth', 'client_id'),
        'client_secret': config.get('auth', 'client_secret')
    }
    if auth_options['service'] == 'github':
        try:
            allowed_orgs = config.get('auth', 'allowed_orgs')
        except ConfigParser.NoOptionError:
            pass
        else:
            allowed_orgs = [org.strip() for org in allowed_orgs.split(',')]
            auth_options['allowed_orgs'] = allowed_orgs

    app = janitor_factory(options, auth_options)
    httpd = WSGIServer((host, port), app)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
