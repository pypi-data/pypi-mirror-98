# -*- coding: utf-8 -*-

import os

import passlib.hash
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from framework.apps import get_app_path
from framework.utils import mkdirs
from myadmin.models import Role, User, UserInfo

# mail 字段是 mindoc 需要
cn_tpl = '''dn: cn={cn},ou=people,dc=example,dc=com
objectClass: posixAccount
uid: {uid}
cn: {cn}
sn: {sn}
alias: {alias}
uidNumber: {uidNumber}
status: {status}
email: {email}
mail: {email}
employeeId: {employee_id}
userPassword: {userPassword}


'''

ou_role_tpl = '''dn: cn={cn},ou=role,dc=example,dc=com
cn: {cn}
gidNumber: {gidnumber}
parent: {parent}
alias: {alias}
description: {desc}
objectclass: posixGroup
objectclass: top
{memberuid}


'''

dc_tpl = '''dn: dc=example,dc=com
objectClass: dcObject
dc: example'''
# sourceStrin=1234546
# passlib.hash.ldap_salted_sha1.encrypt('123456')
# '{SSHA}TgL7DCvwD6UkA4mgcOkEUJf2RdSZ0xqj'

DBPATH = os.path.join(get_app_path('ldap_account'), 'ldiftree.tmp')
OU_PEOPLE_DIR = os.path.join(DBPATH, 'dc=com.dir', 'dc=example.dir', 'ou=people.dir')
OU_ROLE_DIR = os.path.join(DBPATH, 'dc=com.dir', 'dc=example.dir', 'ou=role.dir')
mkdirs(OU_PEOPLE_DIR)
mkdirs(OU_ROLE_DIR)


@receiver(post_save, sender=User, dispatch_uid="user_save_ldap")
def user_save_ldap(sender, instance, **kwargs):
    user: User = instance
    file_name = 'cn=%s.ldif' % user.username
    user_info = user.userinfo_set.first()
    employee_id = email = ''
    if user_info:
        employee_id = user_info.employee_id
        email = user_info.email
    save_path = os.path.join(OU_PEOPLE_DIR, file_name)
    secret = passlib.hash.ldap_salted_sha1.encrypt(user.password)

    if user.status == User.Status.NORMAL:
        with open(save_path, 'w') as f:
            ldap_cn_str = cn_tpl.format(cn=user.username, sn=user.alias[0], uid=user.username, alias=user.alias,
                                        uidNumber=user.id,
                                        userPassword=secret, email=email, employee_id=employee_id, status=user.status)
            f.write(ldap_cn_str)
    else:
        user_delete_ldap(sender, instance)


@receiver(post_delete, sender=User, dispatch_uid="user_delete_ldap")
def user_delete_ldap(sender, instance, **kwargs):
    file_name = 'cn=%s.ldif' % instance.username
    save_path = os.path.join(OU_PEOPLE_DIR, file_name)
    if os.path.exists(save_path):
        os.remove(save_path)


@receiver(post_save, sender=Role, dispatch_uid="role_save_ldap")
def role_save_ldap(sender, instance, **kwargs):
    role = instance
    file_name = 'cn=%s.ldif' % role.name
    if role.type == Role.RoleType.GROUP:
        parent = role.parent.name if role.parent else ''
        save_path = os.path.join(OU_ROLE_DIR, file_name)
        memberuid_list = '\n'.join(['memberUid: %s' % v for v in role.user_set.all().values_list('username')])

        with open(save_path, 'w') as f:
            ldap_cn_str = ou_role_tpl.format(cn=role.name, parent=parent, gidnumber=role.id, alias=role.alias,
                                             desc=role.remark, memberuid=memberuid_list)
            f.write(ldap_cn_str)


@receiver(post_delete, sender=Role, dispatch_uid="role_delete_ldap")
def role_delete_ldap(sender, instance, **kwargs):
    file_name = 'cn=%s.ldif' % instance.name
    save_path = os.path.join(OU_ROLE_DIR, file_name)
    if os.path.exists(save_path):
        os.remove(save_path)


@receiver(post_save, sender=UserInfo, dispatch_uid="user_info_save_ldap")
def user_info_save_ldap(sender, instance, **kwargs):
    user = instance.user
    user_save_ldap(sender, user)


@receiver(post_save, sender=UserInfo, dispatch_uid="user_info_delete_ldap")
def user_info_delete_ldap(sender, instance, **kwargs):
    user = instance.user
    user_delete_ldap(sender, user)

# @receiver(m2m_changed, sender=Admin.role.through, dispatch_uid="user_role_add_ldap")
# def user_role_add(sender,**kwargs):
#     print('user_role_add_ldap')
#     print(sender,kwargs)
#    # print (kwargs['model'].objects.all())
