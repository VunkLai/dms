from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import serializers

from cost_center.models import CostCenter
from employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    centers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Employee
        fields = ['id', 'name', 'centers']


def home(request):
    '''HTML'''
    employees = Employee.objects.all()
    content = {'employees': employees}
    return render(request, 'cost_center/employees.html', content)


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
