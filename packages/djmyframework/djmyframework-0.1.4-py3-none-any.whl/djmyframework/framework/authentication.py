# -*- coding: utf-8 -*-
# @Time : 2021-02-08 19:26
# @Author : xzr
# @File : authentication.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc :


from rest_framework.authentication import SessionAuthentication


class MySessionAuthentication(SessionAuthentication):
    def authenticate(self, request):

        user = getattr(request._request, 'user', None)

    # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        return (user, None)
