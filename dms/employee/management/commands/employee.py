from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from employee.datasource import BPMLoader, CSVLoader
from employee.models import Employee


class Command(BaseCommand):

    LOADERS = {'csv': CSVLoader, 'bpm': BPMLoader}

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('loader', choices=self.LOADERS.keys())

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        '''Update or Create employees'''
        loader = self.LOADERS.get(options['loader'])
        new = Employee.objects.loads(loader=loader)
        total = Employee.objects.count()
        return f'[Employee] Add {new} employee(s), Total {total} employee(s)'
