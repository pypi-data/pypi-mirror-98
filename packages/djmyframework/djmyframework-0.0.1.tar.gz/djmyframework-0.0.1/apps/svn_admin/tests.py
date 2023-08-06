from django.test import TestCase

from myadmin.models import User, Role
from svn_admin.models import SvnPath


# Create your tests here.
class Test(TestCase):
    def setUp(self):
        from django.conf import settings
        settings.DEBUG = False
        self.create_test_svn_path()
        self.create_admins()

    def create_test_svn_path(self):
        m1, _ = SvnPath.objects.get_or_create(project_name='test', path='/', read_member=['a', 'b', 'r'],
                                              write_member=['a', 'b', 'w'])
        m2, _ = SvnPath.objects.get_or_create(project_name='test', path='/test', read_member=['@a', 'b', 'r'],
                                              write_member=['a', 'b', 'w'])
        m3, _ = SvnPath.objects.get_or_create(project_name='test', path='/test', read_member=['a', '@b', 'r'],
                                              write_member=['@group3', '@b', '@w', '@r4'])

    def create_admins(self):
        a1, _ = User.objects.get_or_create(username='username1', password='password1', status=User.Status.NORMAL)
        a2, _ = User.objects.get_or_create(username='username2', password='password2', status=User.Status.NORMAL)
        a3, _ = User.objects.get_or_create(username='username3', password='password3', status=User.Status.NORMAL)
        a4, _ = User.objects.get_or_create(username='username4', password='password4', status=User.Status.NORMAL)
        a5, _ = User.objects.get_or_create(username='username5', password='password5', status=User.Status.NORMAL)


        r1, _ = Role.objects.get_or_create(name='group1', type=Role.RoleType.GROUP)
        r2, _ = Role.objects.get_or_create(name='group2', type=Role.RoleType.GROUP)
        r3, _ = Role.objects.get_or_create(name='group3', type=Role.RoleType.GROUP)

        a1.role.add(*[r1, r2, r3])
        a3.role.add(r1)
        a4.role.add(r2)
        a5.role.add(*[r3])

    def test_sync_user(self):
        SvnPath.sync_user_to_password_db()

    def test_svn_path_authz_db(self):
        SvnPath.sync_svn_path_authz_db()


    def test_get_svn_project(self):
        print(SvnPath.get_svn_project_list())