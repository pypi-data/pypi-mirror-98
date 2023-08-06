# -*- coding: utf-8 -*-
# @Time : 2020-04-27 14:17
# @Author : xzr
# @File : context_processors.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc :

import settings as s


def settings(request):
    return {
            'settings': s
    }
