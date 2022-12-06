from embed_video.fields import EmbedVideoField

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _

from brabbl.accounts.models import Customer, User
from brabbl.utils.models import TimestampedModelMixin, LastActivityMixin, SetOfPropertiesMixin
from . import managers
from easy_thumbnails.files import get_thumbnailer


class Tag(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)

    objects = managers.TagQuerySet.as_manager()

    class Meta:
        unique_together = ('customer', 'name')

    def __str__(self):
        return self.name


class Wording(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.CharField(max_length=1024, blank=True, default='')
    rating_1 = models.CharField(max_length=64, blank=True, default='', help_text=_("very poor"))
    rating_2 = models.CharField(max_length=64, blank=True, default='', help_text=_("poor"))
    rating_3 = models.CharField(max_length=64, blank=True, default='', help_text=_("ok"))
    rating_4 = models.CharField(max_length=64, blank=True, default='', help_text=_("good"))
    rating_5 = models.CharField(max_length=64, blank=True, default='', help_text=_("very good"))
    list_header_contra = models.CharField(max_length=64, blank=True, default='', help_text=_("CONTRA"))
    list_header_pro = models.CharField(max_length=64, blank=True, default='', help_text=_("PRO"))
    header_contra = models.CharField(max_length=64, blank=True, default='', help_text=_("Contra-Argument"))
    header_pro = models.CharField(max_length=64, blank=True, default='', help_text=_("Pro-Argument"))
    button_short_new_contra = models.CharField(verbose_name=_("Button Contra"), max_length=64, blank=True, default='',
                                               help_text=_("Write new argument"))
    button_short_new_pro = models.CharField(verbose_name=_("Button Pro"), max_length=64, blank=True, default='',
                                            help_text=_("Write new argument"))
    button_new_contra = models.CharField(verbose_name=_("Button Contra"), max_length=64, blank=True, default='',
                                         help_text=_("Write new argument"))
    button_new_pro = models.CharField(verbose_name=_("Button Pro"), max_length=64, blank=True, default='',
                                      help_text=_("Write new argument"))
    survey_statement = models.CharField(verbose_name=_("Name singular"), max_length=64, blank=True, default='',
                                        help_text=_("Statement"))
    survey_statements = models.CharField(verbose_name=_("Plural name"), max_length=64, blank=True, default='',
                                         help_text=_("Statements"))
    survey_add_answer_button_top = models.CharField(verbose_name=_("Top button"), max_length=64, blank=True, default='',
                                                    help_text=_("Write new statement"))
    survey_add_answer_button_bottom = models.CharField(verbose_name=_("Bottom button"), max_length=64, blank=True,
                                                       default='', help_text=_("Write new statement"))
    reply_counter = models.CharField(verbose_name=_("Name singular"), max_length=64, blank=True, default='',
                                     help_text=_("Reply"))
    reply_counter_plural = models.CharField(verbose_name=_("Plural name"), max_length=64, blank=True, default='',
                                            help_text=_("Replies"))
    statement_header = models.CharField(max_length=64, blank=True, default='', help_text=_("Reply"))
    statement_list_header = models.CharField(max_length=64, blank=True, default='', help_text=_("Answer"))

    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    objects = managers.WordingQuerySet.as_manager()

    def __str__(self):
        return self.name


class NotificationWordingMessage(models.Model):
    FIELD_LIST = [
        ('notification_registration', _("Notification Email Verification Required")),
        ('notification_logout', _("Notification on Logout")),
        ('notification_signup_required', _("Notification SignUp Required")),
        ('notification_report_posted', _("Notification Report Posted")),
        ('notification_message_posted', _("Notification Message Posted")),
        ('notification_message_updated', _("Notification Message Updated")),
        ('notification_profile_updated', _("Notification Profile Updated")),
        ('notification_reset_password', _("Notification Reset Password")),
        ('hidden_posting_title', _("Hidden posting title")),
        ('hidden_posting_body', _("Hidden posting body")),
        ('notification_discussion_already_completed', _("Notification Discussion Already Completed")),
        ('notification_discussion_not_started', _("Notification Discussion Not Started Yet")),
    ]

    property_model = models.ForeignKey(
        'NotificationWording', related_name='model_properties', on_delete=models.CASCADE)
    key = models.CharField(max_length=64, db_index=True)
    value = models.TextField(blank=True, default="")

    def __str__(self):
        return str(dict(NotificationWordingMessage.FIELD_LIST).get(self.key, 'None'))


class MarkdownWordingMessage(models.Model):
    FIELD_LIST = [
        ('sign_up_title', _("Sign Up Title")),
        ('sign_up_text', _("Sign Up Text")),
        ('login_title', _("Login Title")),
        ('login_text', _("Login Text")),
        ('welcome_title', _("Welcome Title")),
        ('welcome_text_social', _("Welcome Text (after Social-Auth Sign Up)")),
        ('welcome_text_email', _("Welcome Text (after Email Sign Up)")),
        ('barometer_start_sign', _("Barometer Start Sign")),
        ('accept_data_policy_overlay_title', _("Data policy overlay title")),
        ('accept_data_policy_overlay_textbody', _("Data policy overlay body")),
        ('blocking_notification_signup_to_private_account_failed', _("Sign up to private account failed")),
        ('blocking_notification_verification_required', _("Verification required")),
        ('list_of_duplicate_invitation_emails', _("List of duplicate invitation email")),
        ('private_discussions_not_confirmed', _("Private discussions not confirmed")),
        ('private_discussions_not_logged_in', _("Private discussions not logged in")),
    ]
    property_model = models.ForeignKey(
        'NotificationWording', related_name='model_markdown_properties', on_delete=models.CASCADE)
    key = models.CharField(max_length=64, db_index=True)
    value = models.TextField(blank=True, default="")

    def __str__(self):
        return str(dict(MarkdownWordingMessage.FIELD_LIST).get(self.key, 'None'))


class NotificationWording(SetOfPropertiesMixin, models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_("First create a model to see all messages"))

    def save(self, *args, **kwargs):
        super().save(**kwargs)
        properties = self.model_markdown_properties.all()
        SetOfPropertiesMixin.auto_create_delete_properties(self, properties, MarkdownWordingMessage)

    def __str__(self):
        return self.name

    property_model = NotificationWordingMessage


class WordingValue(models.Model):
    CHOICES = (
        (-3, "-3"),
        (-2, "-2"),
        (-1, "-1"),
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
    )

    wording = models.ForeignKey(Wording, related_name='words', on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    value = models.IntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('wording', 'value')

    def __str__(self):
        return self.name


class Discussion(LastActivityMixin,
                 TimestampedModelMixin,
                 models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=256, unique=True)
    source_url = models.URLField(null=True, blank=True, verbose_name='Webpage URL (optional)')
    image = models.ImageField(_("Image"), null=True, blank=True, upload_to='images/discussion/')
    copyright_info = models.CharField(null=True, blank=True, max_length=80)
    image_url = models.URLField(blank=True)
    statement = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=1024, verbose_name='Description (optional)')
    has_barometer = models.BooleanField(default=True)
    has_arguments = models.BooleanField(default=True)
    has_replies = models.BooleanField(default=True)
    multiple_statements_allowed = models.BooleanField(default=False)
    user_can_add_replies = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    discussion_wording = models.ForeignKey(
        Wording, verbose_name=_("Wording"), null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    discussion_users = models.ManyToManyField(User, through='core.DiscussionUser',
                                              through_fields=('discussion', 'user'),
                                              related_name="discussion_user_set")
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    BAROMETER_ALWAYS_SHOW = 1
    BAROMETER_SHOW_FOR_VOTED_USER = 2
    BAROMETER_SHOW_FOR_VOTED_USER_AND_ADMIN = 3

    barometer_behavior = models.IntegerField(
        default=BAROMETER_SHOW_FOR_VOTED_USER_AND_ADMIN, choices=(
            (BAROMETER_ALWAYS_SHOW, _("Barometer always shows the current voting results")),
            (BAROMETER_SHOW_FOR_VOTED_USER, _(
                "Barometer only shows results to users who already voted for this statement")),
            (BAROMETER_SHOW_FOR_VOTED_USER_AND_ADMIN, _(
                "Barometer only shows results to users who already voted for this statement,"
                " and to users with 'Admin' account"))
        )
    )

    objects = managers.DiscussionQuerySet.as_manager()

    @property
    def statement_count(self):
        if self.multiple_statements_allowed:
            return self.statements.visible().count()
        return 0

    @property
    def argument_count(self):
        return sum([statement.arguments.count()
                    for statement in self.statements.all()])

    @property
    def discussion(self):
        return self

    class Meta:
        unique_together = ('external_id', 'customer')

    def __str__(self):
        return self.statement

    def save(self, *args, **kwargs):
        if not self.multiple_statements_allowed:
            self.user_can_add_replies = False
        # strip brabbl-hash from url
        if self.source_url and settings.WIDGET_HASHTAG in self.source_url:
            self.source_url = self.source_url.split('#')[0]
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        thumbnailer = get_thumbnailer(self.image)
        thumbnailer.delete_thumbnails()
        self.image.delete()
        pdfs = self.associated_files.all()
        for pdf in pdfs:
            pdf.delete()
        statements = self.statements.all()
        for statement in statements:
            statement.delete()
        super().delete(*args, **kwargs)


class DiscussionList(TimestampedModelMixin, models.Model):
    SEARCH_BY_SHOW_ALL = 1
    SEARCH_BY_ANY_TAG = 2
    SEARCH_BY_ALL_TAGS = 3
    OPTIONS_SEARCH_BY = (
        (SEARCH_BY_SHOW_ALL, _("Show all")),
        (SEARCH_BY_ANY_TAG, _("Search by any tag")),
        (SEARCH_BY_ALL_TAGS, _("Search by all tags")),
    )
    url = models.URLField(null=True, db_index=True, unique=True)
    name = models.CharField(max_length=160)
    search_by = models.PositiveSmallIntegerField(choices=OPTIONS_SEARCH_BY)
    tags = models.ManyToManyField(Tag, blank=True)
    hide_tag_filter_for_users = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Statement(LastActivityMixin,
                TimestampedModelMixin,
                models.Model):
    STATUS_ACTIVE = 1
    STATUS_HIDDEN = 2
    LIST_OF_STATUSES = (
        (STATUS_ACTIVE, _("Active")),
        (STATUS_HIDDEN, _("Hidden"))
    )
    discussion = models.ForeignKey(Discussion, related_name='statements', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    statement = models.CharField(max_length=1024, blank=True)
    description = models.CharField(null=True, blank=True, max_length=1024, verbose_name='Description (optional)')
    flags = GenericRelation('Flag')
    status = models.PositiveSmallIntegerField(
        default=STATUS_ACTIVE, choices=LIST_OF_STATUSES
    )
    # denormalized from self.barometer_votes
    barometer_count = models.PositiveIntegerField(default=0, editable=False)
    barometer_value = models.DecimalField(decimal_places=1, max_digits=2,
                                          default=0, editable=False)

    image = models.ImageField(_("Image"), null=True, blank=True, upload_to='images/statements/')
    video = EmbedVideoField(_("Video"), null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    copyright_info = models.CharField(null=True, blank=True, max_length=80)

    objects = managers.StatementQuerySet.as_manager()

    @property
    def has_barometer(self):
        return self.discussion.has_barometer

    @property
    def has_arguments(self):
        return self.discussion.has_arguments

    @property
    def has_replies(self):
        return self.discussion.has_replies

    @property
    def reply_count(self):
        return self.arguments.count()

    @property
    def customer(self):
        return self.discussion.customer

    def __str__(self):
        return self.statement

    def save(self, *args, **kwargs):
        if not self.discussion.multiple_statements_allowed:
            self.statement = ''

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        thumbnailer = get_thumbnailer(self.image)
        thumbnailer.delete_thumbnails()
        self.image.delete()
        pdfs = self.statement_associated_files.all()
        for pdf in pdfs:
            pdf.delete()
        super().delete(*args, **kwargs)


class DiscussionUser(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="discussions_set")
    active = models.BooleanField(default=True)


class AssociatedFile(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, blank=True, null=True, related_name="associated_files")
    statement = models.ForeignKey(
        Statement, on_delete=models.CASCADE, blank=True, null=True, related_name="statement_associated_files")
    filename = models.CharField(blank=False, null=False, max_length=512)

    @property
    def name(self):
        filename = self.filename.split('/')[-1]
        return filename[33:]

    @property
    def url(self):
        return self.filename

    def __str__(self):
        return self.filename

    def delete(self):
        fs = FileSystemStorage()
        if fs.exists(self.filename):
            fs.delete(self.filename)

        super(AssociatedFile, self).delete()


class BarometerVote(TimestampedModelMixin, models.Model):
    statement = models.ForeignKey(
        Statement, related_name='barometer_votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=WordingValue.CHOICES)

    class Meta:
        unique_together = ('statement', 'user')


class Argument(LastActivityMixin,
               TimestampedModelMixin,
               models.Model):

    STATUS_ACTIVE = 1
    STATUS_HIDDEN = 2
    LIST_OF_STATUSES = (
        (STATUS_ACTIVE, _("Active")),
        (STATUS_HIDDEN, _("Hidden"))
    )
    statement = models.ForeignKey(
        Statement, related_name='arguments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField()
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE
    )

    title = models.CharField(max_length=1024)
    text = models.TextField(null=True, blank=True)

    flags = GenericRelation('Flag')

    original_title = models.CharField(max_length=1024, null=True, blank=True)
    original_text = models.TextField(null=True, blank=True)

    status = models.PositiveSmallIntegerField(
        default=STATUS_ACTIVE, choices=LIST_OF_STATUSES
    )

    # denormalized from self.ratings
    rating_value = models.DecimalField(
        decimal_places=1, max_digits=2, editable=False,
        default=settings.DEFAULT_USER_RATING)
    rating_count = models.PositiveIntegerField(default=0, editable=False)
    # temporary rating of hidden argument
    original_rating_of_hidden_argument = models.DecimalField(
        decimal_places=1, max_digits=2, editable=False, default=0
    )
    original_rating_count_of_hidden_argument = models.PositiveIntegerField(
        default=0, editable=False
    )

    objects = managers.ArgumentQuerySet.as_manager()

    @property
    def reply_count(self):
        return self.replies.visible().count()

    @property
    def customer(self):
        return self.discussion.customer

    @property
    def discussion(self):
        return self.statement.discussion


class Rating(TimestampedModelMixin, models.Model):
    argument = models.ForeignKey(
        Argument, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=1, max_digits=2, editable=False)

    class Meta:
        unique_together = ('argument', 'user')


class Flag(TimestampedModelMixin, models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('content_type', 'object_id', 'user')
