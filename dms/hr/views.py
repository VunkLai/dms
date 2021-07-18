from dataclasses import dataclass
from typing import Optional

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hr.models import Gateway


@dataclass
class Record:

    name: str
    group: Optional[str]
    date: str = None
    start: str = None
    end: str = None
    office_4f: bool = False
    lab_4f: bool = False
    office_8f: bool = False
    engine_8f: bool = False
    office_10f: bool = False
    engine_10f: bool = False


def render_records(queryset):
    records = {}
    for obj in queryset:
        # New
        if obj not in records:
            records[obj.employee.name] = Record(
                name=obj.employee.name,
                group=obj.employee.group,
                date=obj.date,
                start=obj.date,
            )
        # Update Start, End time
        if records[obj.employee.name].end is None:
            if records[obj.employee.name].start < obj.date:
                records[obj.employee.name].end = obj.date
            else:
                records[obj.employee.name].end = records[obj.employee.name].start
                records[obj.employee.name].start = obj.date
        else:
            if not records[obj.employee.name].start < obj.date:
                records[obj.employee.name].start = obj.date
            if not obj.date < records[obj.employee.name].end:
                records[obj.employee.name].end = obj.date
        # Update Door
        if obj.door in ['4F內大門', '4F外大門']:
            records[obj.employee.name].office_4f = True
        elif obj.door == '4F實驗室門':
            records[obj.employee.name].lab_4f = True
        elif obj.door in ['8F內大門', '8F外大門']:
            records[obj.employee.name].office_8f = True
        elif obj.door == '8F機房':
            records[obj.employee.name].engine_8f = True
        elif obj.door in ['10F內大門', '10F外大門']:
            records[obj.employee.name].office_10f = True
        elif obj.door == '10F機房':
            records[obj.employee.name].engine_10f = True
    return records.values()


def gateway(request, year: int = None, month: int = None, day: int = None
            ) -> HttpResponse:
    date = timezone.localtime().replace(**settings.FOUR_ZEROS)
    if all([year, month, day]):
        date = date.replace(year=year, month=month, day=day)

    dt = 2  # today + yesterday
    if date.isoweekday() == 1:  # Monday is 1 and Sunday is 7
        dt = 4  # Monday, Sunday, Saturday and Friday
    content = {'date': date, 'records': {}}
    for x in range(dt):
        record_date = date - timezone.timedelta(days=x)
        queryset = Gateway.objects.filter_date(date=record_date)
        content['records'][record_date] = render_records(queryset)
    return render(request, 'hr/gateway.html', content)
