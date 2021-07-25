from typing import Dict, Generator, Optional

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.timezone import timedelta

from employee.models import Employee
from hr.serializers import GatewayLogSerializer
from server.datetimes import Datetime
from server.files import File


class GatewayQuerySet(models.QuerySet):

    def group_by(self, field: str) -> models.QuerySet:
        return self.values(field).annotate(models.Count(field)).order_by()

    @property
    def have_4f_office(self) -> bool:
        return self.filter(floor=4, door='辦公室').exists()

    @property
    def have_4f_lab(self) -> bool:
        return self.filter(floor=4, door='實驗室').exists()

    @property
    def have_8f_office(self) -> bool:
        return self.filter(floor=8, door='辦公室').exists()

    @property
    def have_8f_engine(self) -> bool:
        return self.filter(floor=8, door='機房').exists()

    @property
    def have_10f_office(self) -> bool:
        return self.filter(floor=10, door='辦公室').exists()

    @property
    def have_10f_engine(self) -> bool:
        return self.filter(floor=10, door='機房').exists()

    @property
    def start(self) -> timezone.datetime:
        return self.first().date

    @property
    def end(self) -> Optional[timezone.datetime]:
        if self.all().count() == 1:
            return None
        return self.last().date


class GatewayManager(models.Manager):

    def get_queryset(self) -> GatewayQuerySet:
        return GatewayQuerySet(self.model, using=self._db)

    def filter_date(self, date: timezone.datetime) -> Generator[Dict, None, None]:
        date = Datetime(date)
        queryset = self.get_queryset().filter(date__range=date.range())
        for row in queryset.group_by('employee__id'):
            employee_id = row['employee__id']
            employee = Employee.objects.get(id=employee_id)
            records = queryset.filter(employee=employee)
            yield dict(
                name=employee.id,
                group=employee.group,
                date=records.first().date.date(),
                start=records.start,
                end=records.end,
                office_4f=records.have_4f_office,
                lab_4f=records.have_4f_lab,
                office_8f=records.have_8f_office,
                engine_8f=records.have_8f_engine,
                office_10f=records.have_10f_office,
                engine_10f=records.have_10f_engine,
            )


class CardEvent(models.Manager):

    def update_today(self):
        return self.update_data(Datetime.today())

    def update_yesterday(self):
        return self.update_data(Datetime.yesterday())

    @transaction.atomic
    def update_data(self, date: timezone.datetime) -> int:
        file = File(settings.CARD_EVENT_DIR / f'{date.strftime("%Y%m%d")}.log')
        if file.exists():
            queryset = self.filter(date__range=[date, date+timedelta(days=1)])
            queryset.delete()
            for line in file.read():
                serializer = GatewayLogSerializer(data={'log': line, 'date': date})
                if serializer.is_valid():
                    self.create(**serializer.data)
            return queryset.count()
        return 0


class Gateway(models.Model):

    class Meta:
        db_table = 'hr_gateway'
        ordering = ['date', 'employee']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['floor']),
            models.Index(fields=['door']),
        ]

    objects = GatewayManager()
    card_event = CardEvent()

    date = models.DateTimeField()
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField(default=1)
    door = models.CharField(max_length=79)
    card = models.CharField(max_length=30)
