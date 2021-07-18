from pathlib import Path
from typing import Optional

from django.conf import settings
from django.utils import timezone

import pandas
from server.mails import MailServer


def download_the_first_psmc_excel_of_today(folder: Path) -> Optional[Path]:
    # A datetime object corresponding to 00:00:00
    # on the current date in the current time zone
    today = timezone.localtime().replace(**settings.FOUR_ZEROS)

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
                    return folder / filename
        return None
    finally:
        server.disconnect()


def extract_sheets_from_psmc_excel(path: Path) -> Path:
    sheets = ['AZRMFD1', 'AZRX1D1', 'AZSACD1']
    new_excel = path.parent / f'{path.stem}_SDR{path.suffix}'
    # pylint:disable=abstract-class-instantiated
    with pandas.ExcelWriter(new_excel, engine='openpyxl') as writer:
        for sheet in sheets:
            data_frame = pandas.read_excel(path, sheet_name=sheet, header=None)
            data_frame.to_excel(writer, sheet_name=sheet, index=False, header=None)
    return new_excel
