import email
import imaplib
from email import policy
from email.message import EmailMessage
from pathlib import Path
from typing import Generator, Iterable

# import pandas
from django.conf import settings
from django.utils import timezone


class MailServer:

    server = None

    def __init__(self) -> None:
        self.connect()

    def connect(self) -> None:
        self.server = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
        self.server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    def disconnect(self) -> None:
        self.server.close()
        self.server.logout()

    def search(self, mailbox: str, subject: str, limit: int = -1) -> Generator[EmailMessage, None, None]:
        self.server.select(mailbox=mailbox, readonly=True)
        _, data = self.server.search(None, f'(SUBJECT "{subject}")')
        for mail_ids in data:
            for mail_id in mail_ids.split()[limit:]:
                yield from self.fetch(mail_id)

    def fetch(self, mail_id: str) -> Iterable[EmailMessage]:
        _, data = self.server.fetch(mail_id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                yield email.message_from_bytes(
                    response_part[1], policy=policy.default)


def download_the_first_psmc_excel_of_today(folder: Path) -> str:
    # A datetime object corresponding to 00:00:00
    # on the current date in the current time zone
    today = timezone.localtime().replace(**settings.FOUR_ZEROS)

    server = MailServer()
    try:
        subject = '[PSMC Lot Status -12"]AP'
        messages = server.search(mailbox='INBOX', subject=subject, limit=-4)
        for message in messages:
            format = '%a, %d %b %Y %H:%M:%S %z'
            date = timezone.datetime.strptime(message['date'], format)
            if date > today:
                for part in message.iter_attachments():
                    filename = part.get_filename()
                    with open(folder / filename, 'wb') as fw:
                        fw.write(part.get_payload(decode=True))
                    # First only
                    return filename
    finally:
        server.disconnect()
