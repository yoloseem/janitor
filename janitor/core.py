""" :mod:`janitor.core`
    ~~~~~~~~~~~~~~~~~~~

"""

from flask import Flask, send_from_directory
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


def janitor_factory(args, secret_key, auth_options):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    @app.route('/<path:path>', methods=['GET'])
    def serve(path=''):
        return send_from_directory('./', path)

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

    app.wsgi_app = client.wsgi_middleware(app.wsgi_app, secret=secret_key)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.wsgi_app = ELBPingPong(app.wsgi_app)
    return app
