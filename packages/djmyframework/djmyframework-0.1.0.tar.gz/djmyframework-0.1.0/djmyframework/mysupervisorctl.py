#!/usr/bin/env python
# coding=utf-8
# 启动后台服务器的守护进程


import os
import sys


def main():
    pwd = os.getcwd()
    supervisor_configfile = os.path.join(pwd, 'configfile', 'supervisord.ini')
    if not os.path.isfile(supervisor_configfile):
        raise Exception('%s not exists' % supervisor_configfile)
    supervisord_cmd = 'supervisord -c %s' % supervisor_configfile
    cmd = supervisorctl_cmd = 'supervisorctl -c %s' % (supervisor_configfile)

    if len(sys.argv) > 1:

        action = sys.argv[1]
        last_action = sys.argv[-1].strip()

        if last_action in ['log', 'restart', 'stop', 'start']:
            action = 'log'
            sys.argv.pop()

        if action == 'log':
            action = 'tail -f'
        # 改变 supervisorctl reload 为发送 重载信号到进程,实现平滑重启
        if action == 'reload':
            action = 'signal HUP'

        if action == 'reloadall':
            action = 'reload'
        argv_str = ' '.join(sys.argv[2:])
        cmd = '%s %s %s' % (supervisorctl_cmd, action, argv_str)

    is_supervisord_running = os.system(supervisorctl_cmd + ' pid') == 0
    if not is_supervisord_running:
        print('supervisord not running,start now!\n%s' % supervisord_cmd)
        os.system(supervisord_cmd)
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
