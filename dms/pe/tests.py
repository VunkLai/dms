from django.conf import settings
from django.test import TestCase


class MailTestCase(TestCase):

    def test_settings(self):
        self.assertEqual(settings.EMAIL_HOST, 'smtp.office365.com')
        self.assertEqual(settings.EMAIL_PORT, 587)
        self.assertTrue(settings.EMAIL_USE_TLS)

        self.assertTrue(settings.EMAIL_HOST_USER)
        self.assertTrue(settings.EMAIL_HOST_PASSWORD)
