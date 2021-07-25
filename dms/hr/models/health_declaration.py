from typing import Dict, Generator

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from hr import serializers
from hr.gcp import Sheet


class HealthDeclarationManager(models.Manager):
    # pylint:disable=too-few-public-methods

    def working_from_home(self) -> models.QuerySet:
        return self.get_queryset().filter(working_from='在家工作')


class GoogleCloudPlatfromManager(models.Manager):
    # pylint:disable=too-few-public-methods

    @transaction.atomic
    def loads(self, date: timezone.datetime) -> Generator[Dict, None, None]:
        self.filter(date__date=date).delete()
        sheet = Sheet(sheet_key=settings.HEALTH_DECLARATION_SHEET)
        rows = 0
        for row in sheet.rows(cols=11):
            serializer = serializers.HealthDeclaration(data=row)
            if serializer.is_valid():
                if serializer.data['date'].date() == date.date():
                    self.create(**serializer.data)
                    rows += 1
        return rows


class HealthDeclaration(models.Model):

    class Meta:
        db_table = 'hr_health_declaration'
        indexes = [
            models.Index(fields=['working_from']),
            models.Index(fields=['symptom']),
            models.Index(fields=['temperature']),
            models.Index(fields=['risk']),
        ]

    objects = HealthDeclarationManager()
    from_gcp = GoogleCloudPlatfromManager()

    date = models.DateTimeField()
    working_from = models.CharField(max_length=16)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    symptom = models.CharField(max_length=119, default=None, null=True)
    measuring_type = models.CharField(max_length=30)
    temperature = models.FloatField()
    risk = models.CharField(max_length=30)
    row61 = models.TextField(default=None, null=True)
    row62 = models.TextField(default=None, null=True)
    row63 = models.TextField(default=None, null=True)
