#!/usr/bin/env python

import os
import shutil

djframework_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.core.management.utils import get_random_secret_key

settings_text = '''
from __future__ import absolute_import

import os
import sys

DEBUG = True
SECRET_KEY = '%s'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APPS = ['djmyframework']
APPS_ROOT = os.path.join(BASE_DIR, 'apps')

from djmyframework.settings import *

PROJECT_ROOT = BASE_DIR

''' % get_random_secret_key()


def init_djframework():
    target_project_dir = os.getcwd()
    dir_name = 'config'
    config_dir = os.path.join(djframework_dir, dir_name)
    project_dir = target_project_dir
    project_conf_dir = os.path.join(project_dir, dir_name)

    requirements_file = os.path.join(target_project_dir, 'requirements.txt')
    settings_file = os.path.join(project_dir, 'settings.py')
    if not os.path.isfile(requirements_file):
        open(requirements_file).write('')
    if not os.path.isdir(project_conf_dir):
        shutil.copytree(config_dir, project_conf_dir)
        print('add config %s' % project_conf_dir)

        shutil.copyfile(os.path.join(djframework_dir, 'wsgi.py'), os.path.join(project_dir, 'wsgi.py'))
        shutil.copyfile(os.path.join(djframework_dir, 'manage.py'), os.path.join(project_dir, 'manage.py'))
        if not os.path.isfile(settings_file):
            open(os.path.join(project_dir, 'settings.py'), 'w').write(settings_text)
        os.mkdir(os.path.join(project_dir, 'apps'))
    else:
        raise Exception('%s 已经存在' % project_conf_dir)


if __name__ == '__main__':
    os.system('yum install openldap-devel')
    os.system('pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --ignore-installed')
