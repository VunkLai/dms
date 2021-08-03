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
        # TODO: Test Table ASFI01_CostCenter_Copy -> ASFI01_CostCenter
        sql = '''
            SELECT AccountID AS employee_id, CostCenterID AS name
            FROM ASFI01_CostCenter_Copy
        '''
        with pymssql.connect(**settings.BPM_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(sql)
                for row in cursor:
                    yield {
                        'employee': Employee.objects.get(id=row['employee_id']),
                        'name': row['name']
                    }


class BPMAdapter:

    connection = None

    def __init__(self):
        self.connect()

    def connect(self):
        if self.connection is None:
            self.connection = pymssql.connect(**settings.BPM_DATABASE)
        return self.connection

    def insert(self, employee: Employee, center: str):
        # TODO: Test Table ASFI01_CostCenter_Copy -> ASFI01_CostCenter
        # Cols: Region, AccountID, AccountName, DeptID, DeptName, CostCenterID
        sql = """
            INSERT INTO ASFI01_CostCenter_Copy
            VALUES (%d, %s, %s, %d, %s, %s)
            """
        cursor = self.connection.cursor()
        values = employee.values()
        values.append(center)
        cursor.execute(sql, values)

    def delete(self, employee: Employee, center: str):
        # TODO: Test Table ASFI01_CostCenter_Copy -> ASFI01_CostCenter
        # Cols: Region, AccountID, AccountName, DeptID, DeptName, CostCenterID
        sql = """
            DELETE FROM ASFI01_CostCenter_Copy
            WHERE AccountID=%s AND CostCenterID=%s
            """
        cursor = self.connection.cursor()
        cursor.execute(sql, (employee.id, center))
