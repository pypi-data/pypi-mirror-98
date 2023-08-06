# -*- coding: utf-8 -*-
# @Time: 2020-06-02 10:09:54.559700
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema

from framework.filters import MyFilterBackend, MyFilterSerializer, OrderingFilter
from framework.route import Route
from framework.serializer import BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, \
    PaginationSerializer, ParamsSerializer, s
from framework.utils import DATETIMEFORMAT
from framework.views import action, CurdViewSet, notcheck, Request, Response, RspError
from myadmin.models import User


class UserSerializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
    last_time = s.DateTimeField(format=DATETIMEFORMAT, required=False, read_only=True)
    role_alias = s.ListSerializer(child=s.CharField(label=_('角色显示名')), read_only=True, required=False)
    status_alias = s.CharField(source='get_status_display', required=False, read_only=True)

    class Meta:
        model = User
        # fields =  '__all__'
        exclude = ['session_key']
        read_only_fields = ['last_ip', 'create_datetime', 'update_datetime']
        extra_kwargs = {'password': {'write_only': True}}


class ListUserRspSerializer(PaginationSerializer):
    results = UserSerializer(many=True)


@Route('myadmin/user')
class UserSet(CurdViewSet):
    filter_backends = (MyFilterBackend, OrderingFilter)

    serializer_class = UserSerializer
    # 可条件过滤的字段
    filter_fields = ['id', 'role', 'alias', 'username', 'last_ip', 'last_time', 'login_count', 'status',
                     'session_key', 'create_datetime', 'update_datetime']
    # 可排序的字段
    ordering_fields = ['id', 'role', 'alias', 'username', 'last_ip', 'last_time', 'login_count', 'status',
                       'session_key', 'create_datetime', 'update_datetime']

    model = User

    def get_queryset(self):
        return User.objects.all().prefetch_related(*['role']).select_related(*[])

    @swagger_auto_schema(query_serializer=MyFilterSerializer, responses=ListUserRspSerializer)
    def list(self, request, *args, **kwargs):

        return super(UserSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(query_serializer=EditParams, responses=UserSerializer)
    def edit(self, request, *args, **kwargs):
        return super(UserSet, self).edit(request, *args, **kwargs)

    @swagger_auto_schema(query_serializer=IdSerializer, request_body=UserSerializer, responses=UserSerializer)
    def save(self, request, *args, **kwargs):
        if not request.data.get('password', ''):
            request.data.pop('password')
        if not request.data.get('role', ''):
            request.data['role'] = []
            # raise RspError(_('至少选择一个角色'))
        return super(UserSet, self).save(request, *args, **kwargs)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request, *args, **kwargs):
        return super(UserSet, self).delete(request, *args, **kwargs)

    class ChangeStatusSerializer(IdsSerializer):
        status = s.ChoiceField(required=True, choices=User.Status.member_list())

    @swagger_auto_schema('post', request_body=ChangeStatusSerializer)
    @action(['post'])
    def change_status(self, request: Request, **kwargs):
        params = self.ChangeStatusSerializer(request.data)
        if params.id:
            User.objects.filter(id__in=params.id).update(status=params.status)
        return Response()

    class ChangePasswordSerializer(ParamsSerializer):
        old_password = s.CharField(label=_('旧密码'))
        password = s.CharField(label=_('新密码'))
        password2 = s.CharField(label=_('确认密码'))

    @swagger_auto_schema('post', request_body=ChangePasswordSerializer)
    @action(['get', 'post'])
    @notcheck
    def change_password(self, request, **kwargs):
        """
        修改密码
        """
        serializer = self.ChangePasswordSerializer(request.data)
        if self.is_post():
            the_user = request.user
            old_password = serializer.old_password
            new_password1 = serializer.password
            new_password2 = serializer.password2
            if not new_password1 or not new_password2 or not old_password:
                raise RspError(_('密码都不能为空!'))
            elif new_password1 != new_password2:
                raise RspError(_('新密码两次不一样!'))
            else:
                if the_user.password == old_password:
                    the_user.password = new_password1
                    the_user.clean_fields()
                    the_user.save(using='write')
                    from myadmin.views import logout
                    logout(request)
                    return Response(msg=_('修改成功'))
                else:
                    raise RspError(_('旧密码错误'))
        return Response(locals())

    @notcheck
    @action(['post', 'get'])
    def impersonate(self, request, *argv, **kwargs):
        """切换其他管理员,方便调试"""
        if request.REQUEST.get('change_previous') and request.session.get('previous_user_id'):
            request.session['user_id'] = request.session['previous_user_id']
            del request.session['previous_user_id']
            return HttpResponseRedirect('/myadmin/index')

        if not request.user.is_root:
            err_msg = '非管理员'
        else:
            if request.method == 'POST':
                change_user_id = request.POST.get('change_user_id', '')
                change_user = User.objects.get(id=int(change_user_id))
                request.session['previous_user_id'] = request.user.id
                request.session['user_id'] = change_user.id
                return HttpResponseRedirect('/myadmin/index')
        user_list = User.objects.all()
        return Response(locals())

