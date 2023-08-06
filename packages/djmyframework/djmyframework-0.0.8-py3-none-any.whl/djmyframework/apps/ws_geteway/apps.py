# -*- coding: utf-8 -*-

from django.apps import AppConfig

from framework.translation import _


class WsGetewayConfig(AppConfig):
    name = 'ws_geteway'
    verbose_name = _('WebSocket 网关')
