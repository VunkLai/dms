import typing
from abc import ABCMeta, abstractstaticmethod

from django.conf import settings

import pymssql
from employee.models import Employee


class Loader(metaclass=ABCMeta):

    @abstractstaticmethod
    def loads() -> int:
        pass


class BPMLoader(Loader):

    @staticmethod
    def loads() -> typing.Generator:
        sql = '''
            SELECT AccountID AS employee_id, CostCenterID AS name
            FROM ASFI01_CostCenter
        '''
        with pymssql.connect(**settings.BPM_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(sql)
                for row in cursor:
                    yield {
                        'employee': Employee.objects.get(id=row['employee_id']),
                        'name': row['name']
                    }
