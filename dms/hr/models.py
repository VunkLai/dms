from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta

from hr.serializers import GatewayLogSerializer
from server.datetimes import Datetime
from server.files import File


class GatewayManager(models.Manager):
    # pylint:disable=too-few-public-methods

    def filter_date(self, date: timezone.datetime) -> models.QuerySet:
        queryset = self.get_queryset()
        return queryset.filter(date__range=[date, date+timedelta(days=1)])


class CardEvent(models.Manager):

    def update_today(self):
        return self.update_data(Datetime.today())

    def update_yesterday(self):
        return self.update_data(Datetime.yesterday())

    def update_data(self, date: timezone.datetime) -> int:
        queryset = self.filter(date__range=[date, date+timedelta(days=1)])
        queryset.delete()
        file = File(settings.CARD_EVENT_DIR / f'{date.strftime("%Y%m%d")}.log')
        try:
            for line in file.read():
                serializer = GatewayLogSerializer(data={'log': line, 'date': date})
                if serializer.is_valid():
                    self.create(**serializer.data)
            return queryset.count()
        except FileNotFoundError:
            return 0


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
