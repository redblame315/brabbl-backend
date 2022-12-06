from django.core.management.base import BaseCommand
from brabbl.accounts.models import User


class Command(BaseCommand):
    help = 'Sends the newsletter'

    def handle(self, *args, **options):
        for user in User.objects.filter(is_active=True):
            if user.newsmail_schedule in [User.DAILY, User.WEEKLY]:
                user.send_newsmail()
