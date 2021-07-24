from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hr.models import Gateway


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
        content['records'][record_date] = Gateway.objects.filter_date(record_date)
    return render(request, 'hr/gateway.html', content)
