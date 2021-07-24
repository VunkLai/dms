from django.contrib import admin

from hr import models


@admin.register(models.Gateway)
class GatewayModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee_name', 'floor', 'door', 'card')
    list_filter = ('date', 'door', 'floor')
    search_fields = ('employee_name', )

    @admin.display(ordering='employee__first_name')
    def employee_name(self, obj) -> str:
        # pylint:disable=no-self-use
        return obj.employee.name
