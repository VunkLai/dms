from pathlib import Path

from django.conf import settings
from django.test import TestCase


class SettingsTestCase(TestCase):

    def test_settings(self):
        self.assertEqual(settings.EMAIL_HOST, 'smtp.office365.com')
        self.assertEqual(settings.EMAIL_PORT, 587)
        self.assertTrue(settings.EMAIL_USE_TLS)

        self.assertTrue(settings.EMAIL_HOST_USER)
        self.assertTrue(settings.EMAIL_HOST_PASSWORD)

    def test_joy_mail(self):
        self.assertTrue(settings.EMAIL_JOY)
        self.assertIsInstance(settings.EMAIL_JOY, str)

    def test_hr_gateway_owner(self):
        self.assertTrue(settings.EMAIL_HR_GATEWAY_OWNER)
        self.assertIsInstance(settings.EMAIL_HR_GATEWAY_OWNER, str)

    def test_hr_gateway_recipients(self):
        self.assertTrue(settings.EMAIL_HR_GATEWAY_TO)
        self.assertIsInstance(settings.EMAIL_HR_GATEWAY_TO, list)
        self.assertGreater(len(settings.EMAIL_HR_GATEWAY_TO), 0)

    def test_gcp_credential(self):
        self.assertTrue(settings.GCP_CREDENTIAL)
        self.assertIsInstance(settings.GCP_CREDENTIAL, Path)
        self.assertTrue(settings.GCP_CREDENTIAL.is_file())

    def test_health_declaration_sheet(self):
        self.assertTrue(settings.HEALTH_DECLARATION_SHEET)
        self.assertIsInstance(settings.HEALTH_DECLARATION_SHEET, str)
