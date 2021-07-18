import email
import imaplib
from email import policy
from email.message import EmailMessage
from typing import Generator, Iterable

from django.conf import settings


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

    def search(self, mailbox: str, subject: str, limit: int = -1
               ) -> Generator[EmailMessage, None, None]:
        self.server.select(mailbox=mailbox, readonly=True)
        _, data = self.server.search(None, f'(SUBJECT "{subject}")')
        for mail_ids in data:
            for mail_id in mail_ids.split()[limit:]:
                yield from self.fetch(mail_id)

    def fetch(self, mail_id: str) -> Iterable[EmailMessage]:
        _, data = self.server.fetch(mail_id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                # pylint:disable=unsubscriptable-object
                yield email.message_from_bytes(
                    response_part[1], policy=policy.default)
