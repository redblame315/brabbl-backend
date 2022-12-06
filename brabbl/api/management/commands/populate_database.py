from django.core.management.base import BaseCommand

from brabbl.api.fixtures import BrabblFactory


class Command(BaseCommand):
    help = 'Populates the database with some dummy data.'

    def handle(self, *args, **options):
        BrabblFactory.populate_database()
