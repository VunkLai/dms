import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from rest_framework import serializers

from cost_center.models import update_centers
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


@login_required(login_url='/login')
def home(request):
    return render(request, 'cost_center/employees.html')


@require_http_methods(['GET'])
def employees(request):
    if not request.user.is_authenticated:
        data = {'status': 'error', 'message': 'anonymous is not authorized to perform'}
        return JsonResponse(data, status=403)
    queryset = Employee.objects.all()
    serializer = EmployeeSerializer(queryset, many=True)
    return JsonResponse({'employees': serializer.data})


@require_http_methods(['POST'])
def update(request, employee_id: str):
    if not request.user.is_authenticated:
        data = {'status': 'error', 'message': 'anonymous is not authorized to perform'}
        return JsonResponse(data, status=403)
    employee = get_object_or_404(Employee, pk=employee_id)
    try:
        post = json.loads(request.body)
        adds, deletes = update_centers(employee, post['centers'], request.user)
        return JsonResponse({'status': 'ok', 'message': f'add: {adds}, delete: {deletes}'})
    except KeyError:
        return JsonResponse(
            {'status': 'error', 'message': 'centers not found'}, status=400)
    except ValueError:
        return JsonResponse(
            {'status': 'error', 'message': 'centers is empty'}, status=400)
