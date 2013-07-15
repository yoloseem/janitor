""" :mod:`janitor`
    ~~~~~~~~~~~~~~

"""
import argparse
import ConfigParser

from gevent.pywsgi import WSGIServer

from .core import janitor_factory


def run():
    parser = argparse.ArgumentParser(description='Janitor')
    parser.add_argument('-c', '--config', help='configuration file',
                        required=True)
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read(args.config)
    host = config.get('janitor', 'host')
    port = config.getint('janitor', 'port')
    secret_key = config.get('janitor', 'secret_key')

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

    app = janitor_factory(args, secret_key, auth_options)
    httpd = WSGIServer((host, port), app)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
