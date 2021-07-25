from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from django.template.loader import render_to_string
from django.utils import timezone

from hr import views
from hr.models import Gateway
from server.datetimes import Datetime


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['update', 'notify', 'weekly'])

    def handle(self, *args: Any, **options: Any) -> str:
        if options['action'] == 'update':
            return self.update()
        if options['action'] == 'notify':
            call_command('employee', 'build')
            self.update()
            return self.create()
        if options['action'] == 'weekly':
            return self.weekly()
        return '[Gateway] do nothing'

    def update(self):
        today = Gateway.card_event.update_today()
        yesterday = Gateway.card_event.update_yesterday()
        return (
            '[Gateway] '
            f'Today: {today} record(s), '
            f'Yesterday: {yesterday} record(s)'
        )

    def create(self):
        today = Datetime.today()
        content = views.get_records(today)
        template = render_to_string('hr/gateway.html', content)
        email = EmailMessage(
            subject=f'{today.strftime("%F")} 門禁資料',
            body=template,
            from_email=settings.EMAIL_HOST_USER,
            to=settings.EMAIL_HR_GATEWAY_TO,
            bcc=[settings.EMAIL_JOY],
            # cc, reply_to,
        )
        email.content_subtype = 'html'  # Main content is now text/html
        result = email.send()
        return f'result: {result}, recipient: {email.recipients()}'

    def weekly(self):
        today = Datetime.today()
        for x in range(7):
            date = today - timezone.timedelta(days=x)
            rows = Gateway.card_event.update_data(date)
            print(f'{date}: Add {rows} logs')
        return '[Gateway] weekly done'
