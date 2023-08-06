from __future__ import absolute_import

import os


class Command(object):
    help = 'celery 命令'

    def run_from_argv(self, argv):
        argv_str = ' '.join(argv[2:])

        celery_cmd = 'celery -A config.celery_app %s' % argv_str
        print(celery_cmd)
        os.system(celery_cmd)
