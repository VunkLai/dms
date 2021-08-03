from django.contrib import admin

from cost_center import models


@admin.register(models.CostCenter)
class CostCenter(admin.ModelAdmin):

    list_display = ('employee', 'name')
    search_fields = ('name', )


@admin.register(models.UpdateRecords)
class UpdateRecords(admin.ModelAdmin):

    list_display = ('created_at', 'user', 'employee', 'centers')
    list_filter = ('created_at', 'user', 'employee')
    search_fields = ('name', )
