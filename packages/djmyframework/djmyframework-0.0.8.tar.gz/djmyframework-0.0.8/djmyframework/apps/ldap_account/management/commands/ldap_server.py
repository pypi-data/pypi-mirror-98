# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '启动 ldap 服务器'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--port', type=int,
                            dest='port', default=3891,
                            help='端口')
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        port = options.get('port', False)
        from ldap_account.ldap_server import run_ldap_server
        run_ldap_server(port)
