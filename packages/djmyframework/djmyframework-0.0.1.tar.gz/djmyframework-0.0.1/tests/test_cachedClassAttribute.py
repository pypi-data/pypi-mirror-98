# -*- coding: utf-8 -*-
# @Time : 2021-02-25 20:18
# @Author : xzr
# @File : test_cachedClassAttribute.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
from unittest import TestCase

from framework.utils.cache import CachedClassAttribute,CacheAttribute

import functools

from framework.serializer import IdSerializer,EditParams,ParamsSerializer
class TestCachedClassAttribute(TestCase):

    def test_a(self):
        class a(object):
            pp=3

            @CachedClassAttribute
            def cp(cls):
                return cls.__name__

        class b(a):pass

        class c(b):pass

        b.cp
        a.cp

        c.cp

        a1= a()
        a1.cp
        b1= b()
        b1.cp
        c1=c()
        c1.cp
        a=3