# -*- coding: utf-8 -*-
# @Time    : 2021-01-14 14:56
# @Author  : xzr
# @File    : test.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from framework.route import Route
from framework.views import api_get, Response,api_view
from ..tasks import sayhello


@Route()
@api_get()
def test_task(request):
    sayhello.delay('asd', 'asd')
    return Response('ok')
