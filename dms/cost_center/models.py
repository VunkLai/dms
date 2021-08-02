import typing

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction

import pymssql
from employee.models import Employee


class BusinessProcessManagement(models.Manager):

    @staticmethod
    def execute(sql: str) -> typing.Generator:
        # pylint:disable=no-member
        with pymssql.connect(**settings.BPM_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(sql)
                yield from cursor

    def select_all_members(self) -> typing.Generator:
        yield from self.execute('''
            SELECT Region AS region,
                AccountID AS employee_id, AccountName AS employee_name,
                DeptID AS dep_id, DeptName AS dep_name, CostCenterID AS name
            FROM ASFI01_CostCenter
        ''')

    @transaction.atomic
    def loads(self) -> int:
        if self.all().exists():
            raise RuntimeError('Cost Center only loads once')
        for member in self.select_all_members():
            employee = Employee.objects.get(id=member['employee_id'])
            self.create(employee=employee, name=member['name'])
        return self.all().count()

    @staticmethod
    def writer(sql: str):
        # pylint:disable=no-member
        with pymssql.connect(**settings.BPM_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                return cursor.execute(sql)

    def insert(self, employee: Employee, cost_center: str):
        self.writer(f'''
            INSERT INTO ASFI01_CostCenter (
                Region,
                AccountID,
                AccountName,
                DeptID,
                DeptName,
                CostCenterID)
            VALUES (
                {employee.region},
                {employee.id},
                {employee.name},
                {employee.dep_id},
                {employee.dep_name},
                {cost_center}
            );
        ''')

    def delete(self, employee: str, cost_center: str):
        self.writer(f'''
            DELETE FROM ASFI01_CostCenter
            WHERE AccountID={employee.id} AND CostCenterID={cost_center}
        ''')


class CostCenterManager(models.Manager):

    pass


class CostCenter(models.Model):

    class Meta:
        db_table = 'cost_center'

    objects = CostCenterManager()
    from_bpm = BusinessProcessManagement()

    employee = models.ForeignKey('employee.Employee', related_name='centers', on_delete=models.CASCADE)
    name = models.CharField(max_length=79)


class UpdateRecords(models.Model):

    class Meta:
        db_table = 'cost_center_record'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    centers = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


@transaction.atomic
def update_centers(employee: Employee, centers: typing.List[str], user: User):
    UpdateRecords.objects.create(user=user, employee=employee, centers=','.join(centers))
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
