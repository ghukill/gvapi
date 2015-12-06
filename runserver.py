# -*- coding: utf-8 -*-

# gvapi twisted server wrapper
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater, LoopingCall
from twisted.web.server import NOT_DONE_YET
from twisted.web import server, resource
from twisted.python import log

# python modules
import json
import logging
import time

# local
import localConfig
from localConfig import logging


# import flask app
from app import gvapi_app

# gvapi
resource = WSGIResource(reactor, reactor.getThreadPool(), gvapi_app)
site = Site(resource)

# run as script
if __name__ == '__main__':

    # gvapi_app
    logging.debug('starting gvapi - listening on %s' % localConfig.GVAPI_HTTP_PORT)

    # gvapi_app
    reactor.listenTCP(localConfig.GVAPI_HTTP_PORT, site, interface="::")

    # fire reactor
    reactor.run()
