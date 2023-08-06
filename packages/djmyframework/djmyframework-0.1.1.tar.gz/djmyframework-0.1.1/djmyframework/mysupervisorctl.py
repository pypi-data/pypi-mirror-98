#!/usr/bin/env python
# coding=utf-8
# 启动后台服务器的守护进程


import os
import sys

pwd = os.getcwd()
supervisor_config_dir = os.path.join(pwd, 'configfile')

from config.daemon_service import DAEMON_SERVICE_MAP, INET_HTTP_SERVER_LISTEN, INET_HTTP_SERVER_PASSWORD, \
    INET_HTTP_SERVER_USERNAME


def genrate_supervisor_conf(is_force=False):
    supervisor_config_ini_tpl = '''
# http://supervisord.org/configuration.html

[program:{name}]
process_name={name}
command={cmd}
directory=%(here)s/../../
priority=1
autorestart=true
redirect_stderr=true
stdout_logfile=logs/%(program_name)s.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stderr_logfile=logs/%(program_name)s.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel = warn
killasgroup=true
    '''

    supervisord_configs_dir = os.path.join(supervisor_config_dir, 'supervisord.conf.d')
    for name, config in DAEMON_SERVICE_MAP.items():
        config_file_path = os.path.join(supervisord_configs_dir, '%s.ini' % name)
        if not os.path.isfile(config_file_path) or is_force:
            open(config_file_path, 'w').write(supervisor_config_ini_tpl.format(name=name, **config))


def main():
    supervisor_configfile = os.path.join(supervisor_config_dir, 'supervisord.ini')
    if not os.path.isfile(supervisor_configfile):
        raise Exception('%s not exists' % supervisor_configfile)
    supervisord_cmd = 'supervisord -c %s' % supervisor_configfile
    cmd = supervisorctl_cmd = 'supervisorctl -c %s' % (supervisor_configfile)
    os.environ.setdefault('INET_HTTP_SERVER_LISTEN', INET_HTTP_SERVER_LISTEN)
    os.environ.setdefault('INET_HTTP_SERVER_USERNAME', INET_HTTP_SERVER_USERNAME)
    os.environ.setdefault('INET_HTTP_SERVER_PASSWORD', INET_HTTP_SERVER_PASSWORD)
    os.environ.setdefault('PROJECT_ROOT', pwd)

    if len(sys.argv) > 1:
        action = sys.argv[1]
        if len(sys.argv) > 2:
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
    if not is_supervisord_running and action != 'shutdown':
        print('supervisord not running,start now!\n%s' % supervisord_cmd)
        os.system(supervisord_cmd)
    genrate_supervisor_conf(is_force=action=='update')
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
