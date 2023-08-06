#!/usr/bin/env python

import os

if __name__ == '__main__':
    os.system('yum install openldap-devel')
    os.system('pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --ignore-installed')
