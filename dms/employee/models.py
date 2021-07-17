import typing

from django.conf import settings
from django.db import models

import pymssql


class DefaultManager(models.Manager):
    # pylint:disable=too-few-public-methods

    pass


class BusinessProcessManagement(models.Manager):

    @staticmethod
    def execute(sql: str) -> typing.Generator:
        # pylint:disable=no-member
        with pymssql.connect(**settings.MSSQL['BPM']) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(sql)
                yield from cursor

    def select_all_members(self) -> typing.Generator:
        yield from self.execute('''
            SELECT AccountID AS id, DisplayName AS name, EMail AS email
            FROM FSe7en_Org_MemberInfo
        ''')


class Employee(models.Model):

    class Meta:
        db_table = 'employee'
        indexes = [
            models.Index(fields=['group']),
        ]

    objects = DefaultManager()
    from_bpm = BusinessProcessManagement()

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=79)
    email = models.EmailField(**settings.NULLABLE)
    group = models.CharField(max_length=1, **settings.NULLABLE)
