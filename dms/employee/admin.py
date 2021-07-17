from django.contrib import admin

from employee import models


@admin.register(models.Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'group')
    list_filter = ('group', )
    search_fields = ('id', 'name')
