from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from server.datetimes import Datetime


class SettingTestCase(TestCase):

    def test_debug(self):
        # Regardless of the value of the DEBUG setting in your configuration file,
        # all Django tests run with DEBUG=False.
        self.assertFalse(settings.DEBUG)

    def test_secret_key(self):
        self.assertTrue(settings.SECRET_KEY)

    def test_allowed_host(self):
        # The ALLOWED_HOSTS setting is validated when running tests.
        # `ALLOWED_HOSTS = ['testserver']`
        # This allows the test client to differentiate between internal and
        # external URLs.
        self.assertTrue(settings.ALLOWED_HOSTS)
        self.assertGreater(len(settings.ALLOWED_HOSTS), 1)

    def test_db(self):
        db = settings.DATABASES['default']
        self.assertTrue(db)
        self.assertEqual(db['ENGINE'], 'django.db.backends.sqlite3')
        self.assertTrue(db['NAME'])


class DatetimeTestCase(TestCase):

    def test_today(self):
        today = Datetime.today()
        now = timezone.localtime()
        self.assertEqual(today.year, now.year)
        self.assertEqual(today.month, now.month)
        self.assertEqual(today.day, now.day)
        self.assertEqual(today.hour, 0)
        self.assertEqual(today.minute, 0)
        self.assertEqual(today.second, 0)
        self.assertEqual(today.microsecond, 0)

    def test_yesterday(self):
        yesterday = Datetime.yesterday()
        now = timezone.localtime()
        date = now - timezone.timedelta(days=1)
        self.assertEqual(yesterday.year, date.year)
        self.assertEqual(yesterday.month, date.month)
        self.assertEqual(yesterday.day, date.day)
        self.assertEqual(yesterday.hour, 0)
        self.assertEqual(yesterday.minute, 0)
        self.assertEqual(yesterday.second, 0)
        self.assertEqual(yesterday.microsecond, 0)
