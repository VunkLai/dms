from django.urls import path
from django.views.generic import TemplateView

from cost_center import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='cost_center/employees.html')),
    path('employees', views.employees),
    path('update/<str:employee_id>', views.update),
]
