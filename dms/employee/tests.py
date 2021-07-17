import typing
from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

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

    def tearDown(self) -> None:
        Employee.objects.all().delete()

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

    @mock.patch('employee.models.Employee.from_bpm.select_all_members')
    def test_loads(self, members):
        members.return_value = [
            {'id': 'Foo00001', 'name': 'Bar1', 'email': 'bar.1@foo.com'},
            {'id': 'Foo00002', 'name': 'Bar2', 'email': 'bar.2@foo.com', 'group': 'B'},
            {'id': 'Foo00003', 'name': 'Bar3', 'email': None},
        ]
        rows = Employee.from_bpm.loads()
        self.assertIsInstance(rows, int)
        self.assertEqual(rows, 3)

        employees = Employee.objects.all().count()
        self.assertEqual(employees, 3)

        employee = Employee.objects.get(id='Foo00003')
        self.assertFalse(employee.email)

        members.return_value = [
            {'id': 'Foo00001', 'name': 'Bar1', 'email': 'bar.1@foo.com'},
            {'id': 'Foo00003', 'name': 'Bar3', 'email': 'bar.3@foo.com'},
            {'id': 'Foo00004', 'name': 'Bar4', 'email': 'bar.4@foo.com'},
        ]
        rows = Employee.from_bpm.loads()
        self.assertIsInstance(rows, int)
        self.assertEqual(rows, 1)

        employees = Employee.objects.all().count()
        self.assertEqual(employees, 4)

        employee = Employee.objects.get(id='Foo00003')
        self.assertEqual(employee.email, 'bar.3@foo.com')


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
