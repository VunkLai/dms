from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from hr.models import HealthDeclaration
from server.datetimes import Datetime


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['update', 'notify'])

    def handle(self, *args: Any, **options: Any) -> str:
        if options['action'] == 'update':
            rows = HealthDeclaration.from_gcp.loads(
                Datetime.yesterday()-timezone.timedelta(days=1))
            return f'[HR] Add {rows} Health Declaration'
        if options['action'] == 'notify':
            pass
        return '[HR] Health Declaration do nothing'
