from django.conf import settings
from django.test import TestCase


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
