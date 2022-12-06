import pytest
from django.core.management import call_command
from django.core import mail
from .factories import UserFactory
from ..models import User


@pytest.mark.django_db
def test_sending_newsletters():
    call_command('newsmail')
    assert len(mail.outbox) == 0
    UserFactory(newsmail_schedule=User.NEVER)
    user_daily = UserFactory(newsmail_schedule=User.DAILY)
    user_weekly = UserFactory(newsmail_schedule=User.WEEKLY)
    # reset last sent date
    User.objects.update(last_sent=None)
    call_command('newsmail')
    assert len(mail.outbox) == 2

    receivers = [m.to[0] for m in mail.outbox]
    assert [user_daily.email, user_weekly.email] == receivers

    mail.outbox.clear()
    # no new mails should be sent if the command is invoked again on the same day
    call_command('newsmail')
    assert len(mail.outbox) == 0
