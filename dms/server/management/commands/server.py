from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', choices=['build'])

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['action'] == 'build':
            if settings.DEBUG:
                call_command('flush')
                call_command('migrate')
                user = User.objects.create_user('foo', 'foo.bar@gmail.com', 'bar')
                user.is_superuser = True
                user.is_staff = True
                user.save()
            call_command('employee', 'build')
            return '[server] rebuild successfully'
        return '[server] do nothing'
