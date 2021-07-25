from typing import Dict, Generator, Optional
from django.db import models
class HealthDeclarationManager(models.Manager):
    # pylint:disable=too-few-public-methods

    def working_from_home(self):
        return self.get_queryset().filter(working_from='在家工作')

class GoogleCloudPlatfromManager(models.Manager):
    # pylint:disable=too-few-public-methods

    def loads(self, today=None) -> Generator[Dict, None, None]:
        pass
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
    gcp = GoogleCloudPlatfromManager()

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
