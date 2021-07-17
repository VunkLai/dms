from django.test import TestCase

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


class BPMTestCase(TestCase):

    def test_select_all_members_from_bpm(self):
        pass

    def test_execute(self):
        pass
