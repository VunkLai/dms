from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from hr.models import Gateway


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['update'])

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['action'] == 'update':
            try:
                today = Gateway.card_event.update_today()
            except FileNotFoundError:
                today = 0
            try:
                yesterday = Gateway.card_event.update_yesterday()
            except FileNotFoundError:
                yesterday = 0
            return (
                '[Gateway] '
                f'Today: {today} record(s), '
                f'Yesterday: {yesterday} record(s)'
            )
        return '[Gateway] do nothing'