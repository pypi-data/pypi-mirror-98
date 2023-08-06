# -*- coding: utf-8 -*-
# @Time    : 2019-09-03 11:49
# @Author  : xzr
# @File    : resource
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 资源 相关模型


import logging
import typing
from dataclasses import dataclass

from django.db import models
from django.utils.translation import ugettext_lazy as _

from framework.models import BaseModel
from framework.views import Request
from framework.utils import trace_msg
from framework.utils.bitmap import BitMap


class AbsResourceBackend(object):
    @classmethod
    def decode_members(cls, member_str): pass

    @classmethod
    def encode_members(cls, member_list): pass


class BitMapResourceBackend(AbsResourceBackend):
    """资源id 转为16进存储
    """

    @classmethod
    def decode_members(cls, member_str):
        return cls.hex2ids(member_str)

    @classmethod
    def encode_members(cls, member_list):
        return cls.ids2hex(member_list)

    @classmethod
    def ids2hex(cls, id_list):
        hex_str = ''
        if not id_list: return hex_str
        try:
            n_l = [int(x) for x in id_list]
            maxnum = max(n_l) + 1
            bm = BitMap(maxnum)
            bins = []
            for i in n_l:
                bm.set(i)

            hex_str = bm.tohexstring()
        except Exception as e:
            logging.error(trace_msg())

        finally:
            return hex_str

    @classmethod
    def hex2ids(cls, hex_str):
        id_list = set()
        if not hex_str: return id_list
        try:
            bm = BitMap.fromhexstring(hex_str)
            id_list.update(bm.nonzero())
        except Exception as e:
            logging.error(trace_msg())
        finally:
            return id_list


class StrResourceBackend(AbsResourceBackend):
    sep = ','

    @classmethod
    def decode_members(cls, member_str):
        return member_str.split(',')

    @classmethod
    def encode_members(cls, member_list):
        return cls.sep.join((str(x) for x in member_list))


def get_resource_backend(_str):
    if not _str or _str[0] == '0':
        return BitMapResourceBackend
    else:
        return StrResourceBackend


@dataclass
class ModelResource(object):
    """
    模型资源类
    """
    label = ''
    name = ''
    unique_filed_name = 'id'
    alias_lookup = 'alias'
    model_class = None
    template_context = {}
    template = ''
    default_template = 'myadmin/widgets/resource_checkbox.html'
    help_text = ''
    is_inner = False

    @property
    def id_field_lookup(self):
        return '%s_%s' % (self.name, self.unique_filed_name)

    def get_resource_queryset(self, user_model):
        """
        获取资源查询
        :param user_model:
        :return:
        """
        return user_model.get_resource_queryset_from_name(self.name)

    def get_template_context(self, request: Request):
        """
        获取模板上下文
        :param request:
        :return:
        """
        return {}

    def members_handle(self, members):
        """members 都转为 int """
        return (int(i) for i in members)


class Resource(BaseModel):
    """资源
    """
    _resource_map: typing.Dict[
        str, ModelResource] = {}  # {"server":Server,"channel":Channel,"agent":Agent,"server_group":Group}

    name = models.CharField(_("资源名"), max_length=20, null=False, help_text=_('资源简称,只允许字母'))
    role_id = models.IntegerField(_('角色id'), null=True)
    _members = models.TextField(_('资源对象成员列表'))
    __members_cache = None

    class Meta:
        unique_together = (
                ('name', 'role_id'),  # 联合唯一
        )

    @property
    def data_url(self):
        self.__class__._resource_map.get(self.name).model_class.get_list_url()

    def add_member(self, id_or_ids):
        if not isinstance(id, list):
            id_or_ids = [id_or_ids]
        id_or_ids = set(id_or_ids)
        new_ids = self.members
        new_ids |= id_or_ids
        self.members = new_ids

    @property
    def members(self):
        """将16进数据返回id列表
        """
        if self.__members_cache is None:
            _members = get_resource_backend(self._members).decode_members(self._members)
            self.__members_cache = self._resource_map.get(self.name,ModelResource()).members_handle(_members)
        return self.__members_cache

    @members.setter
    def members(self, id_list):
        if not isinstance(id_list, (list, set)):
            id_list = [id_list]
        self._members = StrResourceBackend.encode_members(id_list)

    def __or__(self, other):
        """与位
        @other为资源对象或者资源的成员set表
        """
        if isinstance(other, Resource):
            return self.members.union(other.members)
        return self.members.union(other)

    @classmethod
    def register(cls, model_resource: ModelResource):
        """
        注册资源
        :param modle_name:  名
        :param model_cls:   模型
        :return:
        """
        assert isinstance(model_resource, ModelResource), '%s is not ModelResource subclass ' % model_resource
        assert not model_resource.name in cls._resource_map, 'The same %s already exists' % model_resource.name

        cls._resource_map[model_resource.name] = model_resource

    @classmethod
    def get_resource_map(cls):
        return cls._resource_map

    @classmethod
    def get_model_class(cls, name) -> models.Model:
        return cls.get_model_resource(name).model_class

    @classmethod
    def get_model_resource(cls, name) -> ModelResource:
        return cls._resource_map[name]


class ResourceProxy(object):
    """资源代理,为了在模版里可以使用request.user.resource.xxx
    """

    def __init__(self, user_obj):
        self.user_obj = user_obj

    def get_model_resource_map(self):
        return Resource.get_resource_map()

    def __getattr__(self, name):
        if name != 'user_obj':
            return self.user_obj.get_resource(name)
        else:
            return super(ResourceProxy, self).__getattr__(name)
