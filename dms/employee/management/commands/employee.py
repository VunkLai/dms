from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from employee.models import Employee


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['build', 'sync_bpm'])

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['action'] == 'build':
            rows = Employee.objects.loads()
            total = Employee.objects.count()
            return f'[Employee] Add {rows} member(s) of {total} members'

        if options['action'] == 'sync_bpm':
            rows = Employee.from_bpm.loads()
            total = Employee.objects.count()
            return f'[Employee] Add {rows} member(s) of {total} members'

        return '[Employee] do nothing'
