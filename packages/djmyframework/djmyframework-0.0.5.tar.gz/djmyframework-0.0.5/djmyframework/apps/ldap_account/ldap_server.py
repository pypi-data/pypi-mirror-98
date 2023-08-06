# -*- coding: utf-8 -*-

import os
import sys

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer
import shutil
from ldaptor import ldiftree
from .settings import LDAP_ACCOUNT_SERVER_PORT
from twisted.internet import reactor
from framework.utils import signle_process
from framework.settings import settings


class LDAPServerFactory(ServerFactory):
    protocol = LDAPServer

    def __init__(self, root):
        self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto


from framework.apps import get_app_path

DBPATH = os.path.join(get_app_path('ldap_account'), 'ldiftree')
TMPDBPATH = os.path.join(settings.PROJECT_ROOT, 'ldiftree.tmp')
if not os.path.exists(TMPDBPATH):
    shutil.rmtree(TMPDBPATH, ignore_errors=True)
    shutil.copytree(DBPATH, TMPDBPATH)


def get_db():
    db = ldiftree.LDIFTreeEntry(TMPDBPATH)
    return db


@signle_process.SignleProcessDeco()
def run_ldap_server(port=LDAP_ACCOUNT_SERVER_PORT):
    log.startLogging(sys.stderr)
    # We initialize our tree

    # When the LDAP Server protocol wants to manipulate the DIT, it invokes
    # `root = interfaces.IConnectedLDAPEntry(self.factory)` to get the root
    # of the DIT.  The factory that creates the protocol must therefore
    # be adapted to the IConnectedLDAPEntry interface.
    registerAdapter(
            # lambda x: get_db(),
            lambda x: x.root,

            LDAPServerFactory,
            IConnectedLDAPEntry)

    factory = LDAPServerFactory(get_db())
    factory.debug = True
    application = service.Application("ldaptor-server")
    myService = service.IServiceCollection(application)
    serverEndpointStr = "tcp:{0}".format(port)
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run()


if __name__ == '__main__':
    run_ldap_server()
