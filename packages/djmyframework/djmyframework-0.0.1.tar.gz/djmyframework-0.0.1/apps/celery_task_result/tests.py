


from framework.tests import BaseTestCase
from .tasks import test_live
from django.test import TestCase, override_settings


class TestCeleryTask(BaseTestCase):

    def test_celery_status(self):
        s = test_live.delay()
        print(s)
