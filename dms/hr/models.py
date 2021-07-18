import re
from typing import Any, Dict, Generator, Iterable

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta

from employee.models import Employee


def file_encode_handler(date: timezone.datetime) -> Iterable:
    filename = date.strftime('%Y%m%d')
    path = settings.CARD_EVENT_DIR / f'{filename}.log'
    try:
        with path.open('r', encoding='big5') as fr:
            yield from fr
    except UnicodeDecodeError:
        with path.open('r', encoding='utf8') as fr:
            yield from fr


def log_reader(date: timezone.datetime) -> Generator[Dict, Any, None]:
    # pylint:disable=broad-except
    # just skip the invalid line
    pat = re.compile(r'^.+\) values\s?\((?P<fields>.+)\)$')
    for line in file_encode_handler(date):
        try:
            fields = pat.search(line).group('fields').strip("'").split("','")
            # Date
            time = fields[1].split(':')
            date = date.replace(
                hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
            # Employee
            employee = Employee.objects.get(name=fields[7])
            # Door
            door = fields[5]
            # Card
            card = fields[4]
            yield dict(date=date, employee=employee, door=door, card=card)
        except Exception:
            print(f'[invalid], {line}')


class GatewayManager(models.Manager):
    # pylint:disable=too-few-public-methods

    def filter_date(self, date: timezone.datetime) -> models.QuerySet:
        queryset = self.get_queryset()
        return queryset.filter(date__range=[date, date+timedelta(days=1)])


class CardEvent(models.Manager):

    def update_today(self):
        # A datetime object corresponding to 00:00:00
        # on the current date in the current time zone
        today = timezone.localtime().replace(**settings.FOUR_ZEROS)
        return self.update_data(today)

    def update_yesterday(self):
        # A datetime object corresponding to 00:00:00
        # on the current date in the current time zone
        today = timezone.localtime().replace(**settings.FOUR_ZEROS)
        yesterday = today - timedelta(days=1)
        return self.update_data(yesterday)

    def update_data(self, date: timezone.datetime) -> int:
        queryset = self.filter(date__range=[date, date+timedelta(days=1)])
        queryset.delete()
        for log in log_reader(date):
            self.create(**log)

        return queryset.count()


class Gateway(models.Model):

    class Meta:
        db_table = 'hr_gateway'
        ordering = ['date', 'employee']

    objects = GatewayManager()
    card_event = CardEvent()

    date = models.DateTimeField(db_index=True)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    door = models.CharField(max_length=79)
    card = models.CharField(max_length=30)
