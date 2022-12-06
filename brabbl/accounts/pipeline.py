from uuid import uuid4

from django.shortcuts import get_object_or_404, redirect

from social_core.exceptions import AuthAlreadyAssociated, AuthException
from social_core.pipeline.partial import partial

from brabbl.accounts.models import Customer


USER_FIELDS = ['username', 'email']


def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    customer_token = backend.strategy.session_get('customer_token')
    customer = get_object_or_404(Customer, embed_token=customer_token)
    social = backend.strategy.storage.user.get_social_auth(
        provider, uid, customer
    )
    if social:
        if user and social.user != user:
            msg = 'This {0} account is already in use.'.format(provider)
            raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'customer': customer,
            'user': user,
            'is_new': user is None,
            'new_association': False}


def create_user(strategy, details, customer, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    fields['customer'] = customer
    username = '{}+{}'.format(fields['username'], customer.embed_token)
    while strategy.storage.user.user_exists(username=username):
        username = '{}{}+{}'.format(
            fields['username'], uuid4().hex[:10], customer.embed_token
        )
    fields['username'] = username
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def associate_user(backend, uid, user=None, social=None, *args, **kwargs):
    if user and not social:
        try:
            social = backend.strategy.storage.user.create_social_auth(
                user, uid, backend.name
            )
        except Exception as err:
            if not backend.strategy.storage.is_integrity_error(err):
                raise
            return social_user(backend, uid, user, *args, **kwargs)
        else:
            return {'social': social,
                    'user': social.user,
                    'new_association': True}


def associate_by_email(backend, details, customer, user=None, *args, **kwargs):
    if user:
        return None

    email = details.get('email')
    if email:
        users = list(
            backend.strategy.storage.user.get_users_by_email(email, customer)
        )
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
        else:
            return {'user': users[0]}


def load_extra_data(backend, details, response, uid, user, customer, *args, **kwargs):
    social = kwargs.get('social') or backend.strategy.storage.user.get_social_auth(
        backend.name, uid, customer
    )
    if social:
        extra_data = backend.extra_data(user, uid, response, details,
                                        *args, **kwargs)
        social.set_extra_data(extra_data)


@partial
def finish_auth(strategy, details, user=None, is_new=False, *args, **kwargs):
    if is_new and not strategy.session_get('user_created', False):
        return redirect('welcome-account')
