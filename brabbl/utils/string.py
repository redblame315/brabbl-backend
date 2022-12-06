import random
import string
import datetime

from django.conf import settings
import re


def is_valid_email(email):
    regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.search(regex, email):
        return True
    return False


def random_unique_username(prefix='user'):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    return "{}{}".format(prefix, ts)


def random_string(size=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for __ in range(size))


def add_widget_hashtag(url):
    """Delete existing hashtag, and add widget's hashtag"""
    return url.split("#")[0] + settings.WIDGET_HASHTAG


def duplicate_name(name):
    return "{} New".format(name)


def subset_invitations(invitations, b_invitations):
    b_extended_invitations = []
    for invitation in b_invitations:
        if invitation.endswith("-admin"):
            b_extended_invitations.append(invitation[0: -6])
            b_extended_invitations.append(invitation)
        else:
            b_extended_invitations.append(invitation)
            b_extended_invitations.append(invitation+"-admin")
    result = list(set(invitations)-set(b_extended_invitations))
    return result


def destruct_invitation(invitation):
    if invitation.endswith("-admin"):
        return {
            "email": invitation[0: -6],
            "is_admin": True
        }
    else:
        return {
            "email": invitation,
            "is_admin": False
        }
