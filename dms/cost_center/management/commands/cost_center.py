from typing import Any

from django.core.management.base import BaseCommand

from cost_center.models import CostCenter


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str:
        rows = CostCenter.objects.loads()
        return f'[Cost Center] Sync. {rows} IDs from BMP server'
