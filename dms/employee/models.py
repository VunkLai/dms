import csv
import typing
from pathlib import Path
from typing import Any, Dict, Generator

from django.conf import settings
from django.db import models

import pymssql


def csv_reader(path: Path) -> Generator[Dict, Any, None]:
    try:
        with path.open('r', encoding='big5') as fr:
            data = list(csv.DictReader(fr))
    except UnicodeDecodeError:
        with path.open('r', encoding='utf8') as fr:
            data = list(csv.DictReader(fr))
    for row in data:
        yield dict(
            id=row['employee_id'],
            name=row['employee_name'] or row['employee_name_en'],
            group=row['group']
        )


class DefaultManager(models.Manager):

    def loads(self) -> int:
        path = settings.BASE_DIR.parent / 'tmp/employee/members.csv'
        rows = 0
        for row in csv_reader(path):
            _, created = self.update_or_create(id=row['id'], defaults=row)
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
            SELECT AccountID AS id, DisplayName AS name, EMail AS email
            FROM FSe7en_Org_MemberInfo
        ''')

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
    email = models.EmailField(**settings.NULLABLE)
    group = models.CharField(max_length=1, **settings.NULLABLE)
