Janitor
=======

Janitor is a simple HTTP Server that supports OAuth authentication.

1. Write a configuration file::

    $ cat example.cfg
    [janitor]
    host = 127.0.0.1
    port = 8000
    secret_key = realsecretkey123123 
    base_dir = /path/to/protected/files

    [auth]
    service = github
    client_id = githubapplicationclientid
    client_secret = githubapplicationclientsecret
    allowed_orgs = MyGHOrg

2. Run the app with Janitor::

    $ janitor -c example.cfg
