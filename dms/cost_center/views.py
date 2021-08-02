import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
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


@require_http_methods(['GET'])
def employees(request):
    '''API'''
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse({'employees': serializer.data})


@require_http_methods(['POST'])
def update(request, employee_id: str):
    employee = get_object_or_404(Employee, pk=employee_id)
    try:
        post = json.loads(request.body)
        CostCenter.objects.update_centers(employee, centers=post['centers'])
        return JsonResponse({'status': 'ok', 'message': 'OK'})
    except KeyError:
        return JsonResponse(
            {'status': 'error', 'message': 'centers not found'}, status=400)
    except ValueError:
        return JsonResponse(
            {'status': 'error', 'message': 'centers is empty'}, status=400)
