from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users_api.factory import YamdbUserFactory


class Command(BaseCommand):
    help = 'Creat "number" users (default 30) to users_api app'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int, default=3)

    def handle(self, *args, **options):
        n = options['number']
        users = YamdbUserFactory.create_batch(n)
        for user in users:
            try:
                user.save()
            except IntegrityError:
                n -= 1
                print(f'User {user} already exist. Skipping')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {n} Users'))
