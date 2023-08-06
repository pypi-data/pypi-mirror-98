# -*- coding: utf-8 -*-
# @Time    : 2020-09-15 14:35
# @Author  : xzr
# @File    : user_resource
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from .models import User, Menu, ModelResource, Resource, Role


class UserModelResource(ModelResource):
    name = 'user'
    model_class = User
    is_inner = True

    def get_resource_queryset(self, user_model):
        return user_model.get_manageable_user()


class RoleModelResource(ModelResource):
    name = 'role'
    model_class = Role
    is_inner = True


class MenuModelResource(ModelResource):
    unique_filed_name = 'name'
    name = 'menu'
    model_class = Menu
    is_inner = True

    def members_handle(self,members):
        """菜单是返回字符串列表"""
        return members

Resource.register(UserModelResource())
Resource.register(RoleModelResource())
Resource.register(MenuModelResource())
