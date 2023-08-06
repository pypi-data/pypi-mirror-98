# Create your tests here.
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from ldaptor.protocols.ldap.ldapclient import LDAPClient
from ldaptor.protocols.ldap.ldapsyntax import LDAPEntry
from twisted.internet import defer
from twisted.internet.endpoints import clientFromString, connectProtocol
from twisted.internet.task import react

basedn = 'ou=people,dc=example,dc=com'
binddn = 'cn=test,ou=people,dc=example,dc=com'
bindpw = 'test'

query = '(&(objectClass=posixAccount)(cn=test))'

@defer.inlineCallbacks
def onConnect(client):
    # The following arguments may be also specified as unicode strings
    # but it is recommended to use byte strings for ldaptor objects

    try:
        yield client.bind(binddn, bindpw)
    except Exception as ex:
        print(ex)
        raise
    o = LDAPEntry(client, basedn)
    results = yield o.search(filterText=query)
    for entry in results:
        data = entry.toWire()
        print(data.decode('utf-8'))


def onError(err):
    err.printDetailedTraceback(file=sys.stderr)


def run(reactor):
    # endpoint_str = "tcp:host=183.136.223.85:port=13891"
    endpoint_str = "tcp:host=127.0.0.1:port=3891"
    e = clientFromString(reactor, endpoint_str)
    d = connectProtocol(e, LDAPClient())
    d.addCallback(onConnect)
    d.addErrback(onError)
    return d


if __name__ == '__main__':
    #react(run)
    # https://www.cnblogs.com/linxiyue/p/10250243.html
    import ldap

    con = ldap.initialize('ldap://localhost:3891')
    print(con.simple_bind_s(binddn, 'test'),False)

    results = con.search_s(basedn, ldap.SCOPE_SUBTREE, '(cn=test)',['cn','mail'])
    print(results)
    for dn, entry in results:
        print('Processing', repr(dn))
        print(dn,entry)
    con.unbind()

