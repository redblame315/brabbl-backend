from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

TYPE_CONFIRM = 'confirm_registration'
TYPE_WELCOME = 'welcome'
TYPE_DAILY = 'daily_summary'
TYPE_FORGOT = 'forgot_password'
TYPE_FLAGGING = 'argument_flagging'
TYPE_INVITE = 'invite'
TYPE_NON_ACTIVE_USER_WARNING = 'non_active_user_warning'


def get_default_content_summary(email_type):
    constants = {
        TYPE_CONFIRM: _("""Dear visitor of {{domain}}

we have received your registration.

Please confirm this manually by clicking on the following confirmation link:"""),
        TYPE_DAILY: _("""Hello {{ username }},

there is news on {{domain}}:"""),
        TYPE_FLAGGING: _("""Dear Administrator,

a contribution to the brabbl platform has been flagged"""),
        TYPE_FORGOT: _("""Hello {{ username }},

please click on this link to change your password:"""),
        TYPE_INVITE: _("""Hello.

{{ customer }} invited you on Brabbl."""),
        TYPE_WELCOME: '',
        TYPE_NON_ACTIVE_USER_WARNING: _(
            "Your brabbl account on {{domain}} is not active still. Please activate it by clicking on the following "
            "link. Otherwise, your account and all your arguments and votings will be deleted tonight.")
    }
    return constants[email_type] if email_type in constants else ''


def get_template_by_type(email_type):
    templates = {
        TYPE_CONFIRM: 'mails/verify_registration.txt',
        TYPE_NON_ACTIVE_USER_WARNING: 'mails/verify_registration.txt',
        TYPE_DAILY: 'mails/news_mail.txt',
        TYPE_FLAGGING: 'mails/flag_notification.txt',
        TYPE_FORGOT: 'mails/user_reset_password.txt',
        TYPE_WELCOME: '',
        TYPE_INVITE: 'mails/invite_participants.txt'
    }
    return templates[email_type] if email_type in templates else ''


def send_template(recipients, customer, email_type, context=None, sender=None, **kwargs):
    context = context or {}
    if 'user' in context:
        context['username'] = context['user'].just_username
        context['firstname'] = context['user'].first_name
        context['lastname'] = context['user'].last_name
    context['domain'] = customer.domain
    context['customer_representative_name'] = customer.customer_representative_name
    context['public_customer_name'] = customer.public_customer_name

    if not sender:
        sender = getattr(settings, 'DEFAULT_FROM_EMAIL')

    if not isinstance(recipients, list):
        recipients = [recipients]

    subject = ''
    email_data = {}
    if customer.email_group:
        from brabbl.accounts.models import EmailTemplate
        try:
            email_template = customer.email_group.emailtemplate_set.get(key=email_type)
        except EmailTemplate.DoesNotExist:
            pass
        else:
            subject = render_string_as_template(email_template.subject, context)
            email_data = {
                'content_summary': email_template.text,
                'sign': customer.email_sign,
            }
    if not email_data:
        email_data = {
            'content_summary': get_default_content_summary(email_type),
            'sign': _("Your Brabbl team."),
        }
    email_data = {
        'content_summary': render_string_as_template(email_data['content_summary'], context),
        'sign': render_string_as_template(email_data['sign'], context)
    }
    template = get_template_by_type(email_type)
    context.update(email_data)
    default_subject, content = render_to_string(template, context).split('\n', 1)
    if not subject:
        if not default_subject.lower().startswith('subject:'):
            raise ValueError(
                'Mail template "%s" must start with "Subject:" line' % template)
        subject = default_subject[len('Subject:'):].strip()
    bcc = kwargs.get('bcc', None)
    extra_header = kwargs.get('extra_header', None)
    content = content.strip()

    mail_kwargs = {
        'subject': subject,
        'body': strip_tags(content),
        'from_email': sender,
        'to': recipients,
        'headers': {}
    }
    if sender:
        mail_kwargs['headers'].update({'reply-to': customer.replyto_email})
    if bcc:
        mail_kwargs['bcc'] = bcc
    if extra_header:
        mail_kwargs['headers'].update(extra_header)

    email = EmailMultiAlternatives(**mail_kwargs)
    email.attach_alternative(content, "text/html")
    email.send()


def render_string_as_template(string, context):
    template = Template("{% load url_tags %}" + str(string))
    context = Context(context)
    return template.render(context)
