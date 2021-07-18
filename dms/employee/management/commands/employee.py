from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from employee.models import Employee


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['build', 'sync_bpm'])

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['action'] == 'build':
            try:
                rows = Employee.objects.loads()
                return f'[Employee] Add {rows} member(s)'
            except Exception as e:
                return f'[Employee] Error {e}'

        if options['action'] == 'sync_bpm':
            try:
                rows = Employee.from_bpm.loads()
                return f'[Employee] Add {rows} member(s)'
            except Exception as e:
                return f'[Employee] Error {e}'

        return '[Employee] do nothing'
