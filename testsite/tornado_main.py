#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado_main.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import django.core.handlers.wsgi

from tornado.options import options, define  # , parse_command_line

define('port', type=int, default=8080)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


def main():
    os.environ["DJANGO_SETTINGS_MODULE"] = "testsite.settings"
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application([
        ('/hello-tornado', HelloHandler),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

