from django.conf import settings
from django.db import models, transaction

from employee.datasource import Loader


class EmployeeManager(models.Manager):

    @transaction.atomic
    def loads(self, loader: Loader) -> int:
        rows = 0
        for row in loader.loads():
            _, created = self.update_or_create(id=row['id'], defaults=row)
            if created:
                rows += 1
        return rows


class Employee(models.Model):

    class Meta:
        db_table = 'employee'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['group']),
        ]

    objects = EmployeeManager()

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=79)
    dep_id = models.CharField(max_length=79)
    dep_name = models.CharField(max_length=79)
    email = models.EmailField(**settings.NULLABLE)
    group = models.CharField(max_length=1, **settings.NULLABLE)

    @property
    def region(self) -> str:
        return self.id[:3]
