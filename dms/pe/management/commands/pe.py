from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandParser

from pe import models


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        pass

    def handle(self, *args: Any, **options: Any) -> str:
        excel, date = models.download_the_first_psmc_excel_of_today()
        psmc = models.PsmcExcel.objects.create(
            name=excel.name, date=date, status='new job')
        if excel.is_file():
            psmc.status = 'downloaded'
            psmc.file = excel
            psmc.save()

        new_excel = models.extract_sheets_from_psmc_excel(excel)
        if new_excel.is_file():
            psmc.status = 'extracted'
            psmc.save()

        email = EmailMessage(
            subject='PSMC WIP report',
            from_email=settings.EMAIL_HOST_USER,
            to=settings.EMAIL_PE_PSMC_TO,
            bcc=[settings.EMAIL_JOY],
            # cc, reply_to,
        )
        email.attach_file(new_excel)
        result = email.send(fail_silently=False)
        psmc.status = 'success' if result > 0 else 'failure'
        psmc.save()

        data = {
            'result': result,
            'recipients': email.recipients(),
            'attachments': [attachment[0] for attachment in email.attachments]
        }

        return f'[send] {data}'
