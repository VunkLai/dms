from django.http import JsonResponse
from rest_framework import serializers

from cost_center.models import CostCenter
from employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(source='id')
    employee_name = serializers.CharField(source='name')
    department_id = serializers.CharField(source='dep_id')
    department_name = serializers.CharField(source='dep_name')
    centers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')

    class Meta:
        model = Employee
        fields = [
            'employee_id', 'employee_name', 'department_id', 'department_name',
            'centers'
        ]


def employees(request):
    '''API'''
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse({'employees': serializer.data})


def add(request, employee_id: str, cost_center: str):
    '''API'''
    employee = Employee.objects.get(id=employee_id)
    CostCenter.objects.create(employee=employee, name=cost_center)
    return JsonResponse({'status': 'ok'})
