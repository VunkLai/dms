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

    def test_select_all_members_from_bpm(self):
        pass

    def test_execute(self):
        pass


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
