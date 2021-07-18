from django.contrib import admin

from pe import models


@admin.register(models.PsmcExcel)
class PsmcExcelModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'status', 'file')
    list_filter = ('status', )
    search_fields = ('name', )
