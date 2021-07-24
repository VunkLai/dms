from django.conf import settings
from django.utils import timezone


class Datetime:

    date = None

    def __init__(self, date: timezone.datetime) -> None:
        self.date = date

    def range(self):
        date = self.date.replace(**settings.FOUR_ZEROS)
        return (date, date+timezone.timedelta(days=1))

    @staticmethod
    def today() -> timezone.datetime:
        '''Returns a Today datetime object

        The datetime object corresponding to 00:00:00 in the current time zone
        '''
        return timezone.localtime().replace(**settings.FOUR_ZEROS)

    @classmethod
    def yesterday(cls) -> timezone.datetime:
        return cls.today() - timezone.timedelta(days=1)
