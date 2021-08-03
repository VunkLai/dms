from typing import List, Tuple

from django.contrib.auth.models import User
from django.db import models, transaction

from cost_center.datasource import Loader
from employee.models import Employee


class CostCenterManager(models.Manager):

    @transaction.atomic
    def loads(self, loader: Loader) -> int:
        if self.exists():
            raise RuntimeError('Cost Center must be empty')
        for row in loader.loads():
            self.create(**row)
        return self.count()


class CostCenter(models.Model):

    class Meta:
        db_table = 'cost_center'

    objects = CostCenterManager()

    employee = models.ForeignKey(
        'employee.Employee', related_name='centers', on_delete=models.CASCADE)
    name = models.CharField(max_length=79)


class UpdateRecords(models.Model):

    class Meta:
        db_table = 'cost_center_record'

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    centers = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


@transaction.atomic
def update_centers(employee: Employee, centers: List[str], user: User) -> Tuple[int]:
    UpdateRecords.objects.create(
        user=user, employee=employee, centers=','.join(centers))
    deletes = 0
    for center in employee.centers.all():
        if not center.name in centers:
            center.delete()
            deletes += 1
    adds = 0
    for center_name in centers:
        if not employee.centers.filter(name=center_name).exists():
            CostCenter.objects.create(employee=employee, name=center_name)
            adds += 1
    return adds, deletes
