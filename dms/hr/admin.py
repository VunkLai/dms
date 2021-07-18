from django.contrib import admin

from hr import models


@admin.register(models.Gateway)
class GatewayModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee_name', 'door', 'card')
    list_filter = ('date', 'door')
    search_fields = ('employee_name', )

    @admin.display(ordering='employee__first_name')
    def employee_name(self, obj) -> str:
        return obj.employee.name
