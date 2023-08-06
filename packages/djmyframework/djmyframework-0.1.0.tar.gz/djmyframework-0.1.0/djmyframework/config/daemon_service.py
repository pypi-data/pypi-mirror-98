#!/usr/bin/env python
# coding=utf-8
# 启动后台服务器的守护进程


DAEMON_SERVICE_MAP = {
        "statistic"  : {"cmd": "python -u manage.py StatisticCron -c", "remark": "统计后台服务"},
        "ldap"       : {"cmd": "python3 -u manage.py ldap_server ", "remark": "ldap 服务"},
        "celery_task": {"cmd": "celery -A celery_app worker -l info -E", "remark": "celery 任务 服务"},
        "celery_cron": {"cmd": "celery -A celery_app worker -B -l info -Q cron", "remark": "celery 定时任务 服务"},
}
