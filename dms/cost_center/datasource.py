import typing
from abc import ABCMeta, abstractmethod

from django.conf import settings

import pymssql
from employee.models import Employee


class Loader(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def loads() -> int:
        pass


class BPMLoader(Loader):

    @staticmethod
    def loads() -> typing.Generator:
        # pylint:disable=no-member
        # E1101: Module 'pymssql' has no 'connect' member (no-member)
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
