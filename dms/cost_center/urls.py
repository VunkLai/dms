from django.urls import path

from cost_center import views

urlpatterns = [
    path('', views.home),
    path('employees', views.employees),
]
