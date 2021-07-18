from pathlib import Path
from typing import Optional

from django.conf import settings
from django.db import models
from django.utils import timezone

import pandas
from server.mails import MailServer


def psmc_folder():
    return settings.BASE_DIR.parent / 'tmp' / 'excels'


class PsmcExcel(models.Model):

    class Meta:
        db_table = 'pe_psmc_excel'
        ordering = ['date']

    name = models.CharField(max_length=30, unique=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=30, **settings.NULLABLE)
    file = models.FilePathField(path=psmc_folder, **settings.NULLABLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def download_the_first_psmc_excel_of_today() -> Optional[Path]:
    # A datetime object corresponding to 00:00:00
    # on the current date in the current time zone
    today = timezone.localtime().replace(**settings.FOUR_ZEROS)

    folder = psmc_folder()
    folder.mkdir(parents=True, exist_ok=True)
    server = MailServer()
    try:
        subject = '[PSMC Lot Status -12"]AP'
        messages = server.search(mailbox='INBOX', subject=subject, limit=-4)
        for message in messages:
            date = timezone.datetime.strptime(
                message['date'], '%a, %d %b %Y %H:%M:%S %z')
            if date > today:
                for part in message.iter_attachments():
                    filename = part.get_filename()
                    with open(folder / filename, 'wb') as fw:
                        fw.write(part.get_payload(decode=True))
                    # First only
                    return folder / filename, date
        return None, today
    finally:
        server.disconnect()


def extract_sheets_from_psmc_excel(path: Path) -> Path:
    sheets = ['AZRMFD1', 'AZRX1D1', 'AZSACD1']
    new_excel = path.parent / f'{path.stem}_SDR{path.suffix}'
    # pylint:disable=abstract-class-instantiated
    with pandas.ExcelWriter(new_excel, engine='openpyxl') as writer:
        for sheet in sheets:
            data_frame = pandas.read_excel(
                path, sheet_name=sheet, header=None, engine='openpyxl')
            data_frame.to_excel(writer, sheet_name=sheet, index=False, header=None)
    return new_excel
