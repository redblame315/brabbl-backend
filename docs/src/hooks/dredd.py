# init django env
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brabbl.conf.tests_dredd")

import django
import dredd_hooks as hooks
import json
import re
from django.conf import settings
from django.core.management import call_command

from brabbl.api.fixtures import BrabblFactory


def replace_in_body(transaction, key, value):
    try:
        body = json.loads(transaction['request']['body'])
    except (KeyError, ValueError):
        return

    if key in body:
        body[key] = value
        transaction['request']['body'] = json.dumps(body)


def replace_lookup_value(transaction, value, regex=r'.*/(\d+)/.*'):
    match = re.match(regex, transaction['fullPath'])
    if match:
        to_replace = match.groups()[0]
        transaction['fullPath'] = transaction['fullPath'].replace(to_replace, str(value))


factory = BrabblFactory()


@hooks.before_all
def before_all_hooks(transaction):
    print("initialize django")
    django.setup()
    call_command('migrate')


@hooks.after_all
def after_all_hooks(transaction):
    os.remove(settings.DATABASES['default']['NAME'])


@hooks.before_each
def add_trailing_slash(transaction):
    if not transaction['fullPath'].endswith('/'):
        transaction['fullPath'] += '/'


@hooks.before_each
def override_customer(transaction):
    headers = transaction['request']['headers']
    if 'X-Brabbl-Token' in headers:
        headers['X-Brabbl-Token'] = factory.customer.embed_token


@hooks.before_each
def override_auth(transaction):
    headers = transaction['request']['headers']
    if 'Authorization' in headers:
        headers['Authorization'] = 'Token {0}'.format(factory.user_token)


@hooks.before_each
def clear_existing_object(transaction):
    factory.clear()


@hooks.before('Account > Register > Register User')
def override_user_credentials(transaction):
    replace_in_body(transaction, 'username', BrabblFactory.USER_USERNAME)
    replace_in_body(transaction, 'password', BrabblFactory.USER_PASSWORD)


@hooks.before('Account > Reset Password > Reset Password')
def reset_password(transaction):
    user = factory.user
    replace_in_body(transaction, 'email', user.email)


@hooks.before('Account > Login > Authenticate')
def generate_user(transaction):
    factory.user
    override_user_credentials(transaction)


@hooks.before('Tags > Tags > Create Tag')
def create_tags(transaction):
    user = factory.user
    user.is_staff = True
    user.save()


@hooks.before('Tags > Tags > List Tags')
def generate_tags(transaction):
    factory.tags


@hooks.before('Wording > Wording > Get Wording')
def generate_wording(transaction):
    wording = factory.wording
    replace_lookup_value(transaction, wording.pk)


@hooks.before('Wording > Wordings > List Wordings')
def generate_wording_list(transaction):
    factory.wording


@hooks.before('Discussions > Discussion > Get Discussion')
def generate_discussion_get(transaction):
    discussion = factory.simple_discussion
    replace_lookup_value(transaction, discussion.external_id, regex=r'.*/([\d\w]+)/$')


@hooks.before('Discussions > Discussion > Update Discussion')
def update_discussion(transaction):
    discussion = factory.simple_discussion
    user = factory.user
    user.is_staff = True
    user.save()
    replace_lookup_value(transaction, discussion.external_id, regex=r'.*/([\d\w]+)/$')


@hooks.before('Discussions > Discussion > Hide Discussion')
def hide_discussion(transaction):
    discussion = factory.simple_discussion
    user = factory.user
    user.is_staff = True
    user.save()
    replace_lookup_value(transaction, discussion.external_id, regex=r'.*/([\d\w]+)/$')


@hooks.before('Discussions > Discussions > Create Discussion')
def create_discussion(transaction):
    user = factory.user
    user.is_staff = True
    user.save()
    replace_in_body(transaction, 'wording', factory.wording.id)


@hooks.before('Statements > Statement > Get Statement')
def get_statement(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    replace_in_body(transaction, 'discussion_id', discussion.external_id)
    replace_lookup_value(transaction, statement.id)


@hooks.before('Statements > Statement > Update Statement')
def update_statement(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    statement.arguments.all().delete()
    statement.last_related_activity = None
    statement.save()
    replace_lookup_value(transaction, statement.id)


@hooks.before('Statements > Statement > Hide Statement')
def hide_statement(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    statement.arguments.all().delete()
    statement.last_related_activity = None
    statement.save()
    replace_lookup_value(transaction, statement.id)


@hooks.before('Statements > Statements > Create Statement')
def create_statement(transaction):
    discussion = factory.complex_discussion
    replace_in_body(transaction, 'discussion_id', discussion.external_id)


@hooks.before('Discussions > Discussions > List Discussions')
def generate_discussion_list(transaction):
    factory.simple_discussion
    factory.complex_discussion


@hooks.before('Arguments > Arguments > Create Argument')
def create_argument(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    replace_in_body(transaction, 'statement_id', statement.id)
    replace_in_body(transaction, 'reply_to', argument.id)


@hooks.before('Arguments > Argument > Get Argument')
def get_argument(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    replace_lookup_value(transaction, argument.id)


@hooks.before('Arguments > Argument > Update Argument')
def update_argument(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    argument.last_related_activity = None
    argument.save()
    replace_lookup_value(transaction, argument.id)


@hooks.before('Arguments > Argument > Hide Argument')
def hide_argument(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    argument.last_related_activity = None
    argument.save()
    replace_lookup_value(transaction, argument.id)


@hooks.before('Arguments > Replies > Get Replies')
def get_argument_replies(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    replace_lookup_value(transaction, argument.id)


@hooks.before('Statements > Barometer > Vote for statement')
def statement_vote(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    replace_lookup_value(transaction, statement.id)


@hooks.before('Arguments > Rating > Rate Argument')
def argument_rating(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]
    replace_lookup_value(transaction, argument.id)


@hooks.before('Flagging > Flag > Flag Argument')
def flag_argument(transaction):
    discussion = factory.simple_discussion
    statement = discussion.statements.all()[0]
    argument = statement.arguments.all()[0]

    replace_in_body(transaction, 'type', 'argument')
    replace_in_body(transaction, 'id', argument.id)
