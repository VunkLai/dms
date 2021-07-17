import typing
from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

import pymssql
from employee.admin import EmployeeModelAdmin
from employee.models import Employee


class ModelTestCase(TestCase):

    def tearDown(self) -> None:
        Employee.objects.all().delete()

    def test_nullable_fields(self):
        employee = Employee.objects.create(id='Foo123', name='Bar')
        self.assertEqual(employee.id, 'Foo123')
        self.assertEqual(employee.name, 'Bar')
        self.assertEqual(employee.email, None)
        self.assertEqual(employee.group, None)


class BPMManagerTestCase(TestCase):

    @mock.patch('employee.models.Employee.from_bpm.execute')
    def test_select_all_members_from_bpm(self, execute):
        execute.return_value = ['foo', 'bar']
        rows = Employee.from_bpm.select_all_members()
        self.assertIsInstance(rows, typing.Generator)
        self.assertEqual(len(list(rows)), 2)

    @mock.patch('employee.models.pymssql.connect')
    def test_execute(self, db):
        db.cursor.execute.return_value = ['foo', 'bar']
        rows = Employee.from_bpm.execute('SELECT foo FROM bar')
        self.assertIsInstance(rows, typing.Generator)
        # TODO: the patch of pymssql is incomplete
        # self.assertEqual(len(list(rows)), 2)


class ModelAdminTestCase(TestCase):

    def setUp(self):
        site = AdminSite()
        self.page = EmployeeModelAdmin(Employee, site)

    def test_list_display(self):
        fields = ('id', 'name', 'email', 'group')
        for field in fields:
            self.assertIn(field, self.page.list_display)

    def test_list_filter(self):
        fields = ('group', )
        for field in fields:
            self.assertIn(field, self.page.list_filter)

    def test_search_fields(self):
        fields = ('id', 'name', )
        for field in fields:
            self.assertIn(field, self.page.search_fields)
