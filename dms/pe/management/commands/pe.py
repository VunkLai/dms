from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.management.base import BaseCommand

from pe import models


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str:
        excel, date = models.download_the_first_psmc_excel_of_today()
        psmc = models.PsmcExcel.objects.create(
            name=str(date), date=date, status='new job')
        if excel is None:
            result = send_mail(
                subject='[Error] PSMC excel not Found',
                message=f'date: {date}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_PE_PSMC_OWNER],
            )
            psmc.status = f'attachment not found, send: {result}'
            psmc.save()
            return f'[PE] PSMC {psmc.status}'
        else:
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
        if result > 0:
            psmc.status = f'success, result: {result}'
            psmc.save()
        else:
            psmc.status = f'failure, result: {result}'
            psmc.save()

        data = {
            'result': result,
            'recipients': email.recipients(),
            'attachments': [attachment[0] for attachment in email.attachments]
        }
        return f'[PE] PSMC {data}'
