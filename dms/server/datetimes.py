from django.conf import settings
from django.utils import timezone


class Datetime:

    @staticmethod
    def today() -> timezone.datetime:
        '''Returns a Today datetime object

        The datetime object corresponding to 00:00:00 in the current time zone
        '''
        return timezone.localtime().replace(**settings.FOUR_ZEROS)

    @classmethod
    def yesterday(cls) -> timezone.datetime:
        return cls.today() - timezone.timedelta(days=1)
