from django.conf import settings
from django.test import TestCase


class MailSettingsTestCase(TestCase):

    def test_settings(self):
        self.assertEqual(settings.EMAIL_HOST, 'smtp.office365.com')
        self.assertEqual(settings.EMAIL_PORT, 587)
        self.assertTrue(settings.EMAIL_USE_TLS)

        self.assertTrue(settings.EMAIL_HOST_USER)
        self.assertTrue(settings.EMAIL_HOST_PASSWORD)

    def test_joy_mail(self):
        self.assertTrue(settings.EMAIL_JOY)
        self.assertIsInstance(settings.EMAIL_JOY, str)

    def test_pe_psmc_owner(self):
        self.assertTrue(settings.EMAIL_PE_PSMC_OWNER)
        self.assertIsInstance(settings.EMAIL_PE_PSMC_OWNER, str)

    def test_pe_psmc_recipients(self):
        self.assertTrue(settings.EMAIL_PE_PSMC_TO)
        self.assertIsInstance(settings.EMAIL_PE_PSMC_TO, list)
        self.assertGreater(len(settings.EMAIL_PE_PSMC_TO), 0)
