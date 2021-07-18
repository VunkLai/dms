from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from pe import models


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        pass

    def handle(self, *args: Any, **options: Any) -> str:
        tmp = Path('/tmp/excels')
        tmp.mkdir(parents=True, exist_ok=True)
        excel_name = models.download_the_first_psmc_excel_of_today(folder=tmp)
        return f'[download], {excel_name}'
