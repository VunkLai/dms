from django.urls import path

from hr import views

urlpatterns = [
    path('gateway/', views.gateway),
    path('gateway/weekly', views.weekly),
    path('gateway/<int:year>/<int:month>/<int:day>', views.gateway),
    path('employee/', views.employee),
]
