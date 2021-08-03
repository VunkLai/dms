import typing
from abc import ABCMeta, abstractstaticmethod

from django.conf import settings

import pymssql
from server.files import CSVFile


class Loader(metaclass=ABCMeta):

    @abstractstaticmethod
    def loads() -> int:
        pass


class CSVLoader(Loader):

    @staticmethod
    def loads() -> typing.Generator:
        path = settings.BASE_DIR.parent / 'tmp/employee/members.csv'
        csv = CSVFile(path)
        for row in csv.read():
            name = row.pop('name', None)
            name_en = row.pop('name_en', None)
            row['name'] = name or name_en
            yield row


class BPMLoader(Loader):

    @staticmethod
    def loads() -> typing.Generator:
        sql = '''
            SELECT DISTINCT M.AccountID AS id, M.DisplayName AS name,
                D.DeptID AS dep_id, D.DisplayName DName AS dep_name
            FROM FSe7en_Org_MemberStruct S
            LEFT JOIN FSe7en_Lang_MemberInfo M on M.AccountID = S.AccountID
            LEFT JOIN FSe7en_Lang_DeptInfo D on S.DeptID = D.DeptID
            WHERE M.Lang='zh-tw' AND D.Lang='zh-tw' AND S.Version='3' AND S.IsMainJob='1'
            AND (M.AccountID!='administrator' AND M.AccountID!='apm.audit1' AND M.AccountID!='apm.audit2')
        '''
        with pymssql.connect(**settings.BPM_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(sql)
                yield from cursor
