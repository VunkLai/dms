import typing

from django.conf import settings
from django.db import models, transaction

import pymssql
from employee.serializers import CSVSerializer
from server.files import CSVFile


class DefaultManager(models.Manager):

    @transaction.atomic
    def loads(self) -> int:
        path = settings.BASE_DIR.parent / 'tmp/employee/members.csv'
        csv = CSVFile(path)
        rows = 0
        for row in csv.read():
            serializer = CSVSerializer(data=row)
            if serializer.is_valid():
                _, created = self.update_or_create(
                    id=serializer.data['id'], defaults=serializer.data)
                if created:
                    rows += 1
        return rows


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
            SELECT DISTINCT M.AccountID AS id, M.DisplayName AS name,
                D.DeptID AS dep_id, D.DisplayName DName AS dep_name
            FROM FSe7en_Org_MemberStruct S
            LEFT JOIN FSe7en_Lang_MemberInfo M on M.AccountID = S.AccountID
            LEFT JOIN FSe7en_Lang_DeptInfo D on S.DeptID = D.DeptID
            WHERE M.Lang='zh-tw' AND D.Lang='zh-tw' AND S.Version='3' AND S.IsMainJob='1'
            AND (M.AccountID!='administrator' AND M.AccountID!='apm.audit1' AND M.AccountID!='apm.audit2')
        ''')

    @transaction.atomic
    def loads(self) -> int:
        rows = 0
        for member in self.select_all_members():
            _, created = self.update_or_create(id=member['id'], defaults=member)
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

    objects = DefaultManager()
    from_bpm = BusinessProcessManagement()

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=79)
    dep_id = models.CharField(max_length=79)
    dep_name = models.CharField(max_length=79)
    email = models.EmailField(**settings.NULLABLE)
    group = models.CharField(max_length=1, **settings.NULLABLE)

    @property
    def region(self):
        return self.id[:3]
