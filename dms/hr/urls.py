from django.urls import path

from hr import views

urlpatterns = [
    path('gateway/', views.gateway),
    path('gateway/<int:year>/<int:month>/<int:day>', views.gateway),
]
