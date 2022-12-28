from embed_video.backends import YoutubeBackend
from rest_framework import exceptions, serializers
from django.core.files.storage import FileSystemStorage

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from brabbl.accounts.models import Customer, CustomerUserInfoSettings, User
from brabbl.utils.models import get_thumbnail_url
from brabbl.utils.serializers import (
    Base64ImageField, NonNullSerializerMixin, PermissionSerializerMixin
)
from . import models
from brabbl.utils.string import random_string
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.utils import html


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, qs):
        return [tag.name for tag in qs.all()]

    def to_internal_value(self, data):
        customer = self.context['request'].customer
        tags = []
        for tag in data:
            tag, __ = models.Tag.objects.get_or_create(
                customer=customer,
                name=tag)
            tags.append(tag)
        return tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data.update({
            'customer': self.context['request'].customer,
        })
        return super().create(validated_data)


class WordingValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WordingValue
        fields = ('name', 'value')


class WordingSerializer(serializers.ModelSerializer):
    words = WordingValueSerializer(many=True)

    class Meta:
        model = models.Wording
        exclude = ['language']


class NotificationWordingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationWordingMessage
        fields = ('key', 'value')


class MarkdownWordingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarkdownWordingMessage
        fields = ('key', 'value')


class NotificationWordingSerializer(serializers.ModelSerializer):
    notification_wording_messages = NotificationWordingMessageSerializer(
        many=True, source='model_properties'
    )
    markdown_wording_messages = MarkdownWordingMessageSerializer(
        many=True, source='model_markdown_properties'
    )

    class Meta:
        model = models.NotificationWording
        fields = '__all__'


class RatingSerializer(serializers.Serializer):
    rating = serializers.FloatField(min_value=1, max_value=5)

    def validate_rating(self, rating):
        decimal = rating * 10 % 10
        if decimal != 0 and decimal != 5:
            raise serializers.ValidationError(
                _("There are only whole or half numbers allowed."))

        return rating


class StatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=models.Argument.LIST_OF_STATUSES)


class ArgumentRatingSerializer(NonNullSerializerMixin, serializers.ModelSerializer):
    count = serializers.IntegerField(source='rating_count')
    rating = serializers.FloatField(source='rating_value')
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = models.BarometerVote
        fields = ('count', 'rating', 'user_rating')
        read_only_fields = ('count', 'rating', 'user_rating')

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return None

        try:
            rating = obj.ratings.get(user=user)
        except models.Rating.DoesNotExist:
            return None
        return rating.value


class ArgumentSerializer(serializers.ModelSerializer):
    statement_id = serializers.IntegerField(source='statement.id', required=True)
    created_by = serializers.CharField(source='created_by.display_name', read_only=True)
    rating = serializers.FloatField(source='rating_value', read_only=True)
    is_pro = serializers.BooleanField(required=True)
    # NOTE: queryset will be restricted in `get_fields`
    reply_to = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=models.Argument.objects.visible())
    rating = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    is_deletable = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = models.Argument
        fields = (
            'id', 'created_at', 'created_by', 'is_pro', 'title', 'statement_id',
            'text', 'rating', 'reply_count', 'reply_to', 'is_editable', 'is_deletable', 'status', 'author')
        read_only_fields = (
            'id', 'created_at', 'created_by', 'rating', 'reply_count', 'author')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        # PrimaryKeyRelatedField requires a queryset
        # But since we have no access to the customer while constructing,
        # we have to override the queryset here.
        customer = self.context['request'].customer
        qs = models.Argument.objects.for_customer(customer).visible()
        fields['reply_to'].queryset = qs
        return fields

    def check_permission(self, obj, permission):
        success = True
        request = self.context['request']
        if request.user.is_anonymous:
            success = False
        if not request.user.has_perm(permission):
            if timezone.now() - obj.created_at > timedelta(minutes=30):
                success = False
            if obj.last_related_activity is not None:
                success = False
            if request.user != obj.created_by:
                success = False
        return success

    def get_is_deletable(self, obj):
        return self.check_permission(obj, 'core.delete_argument')

    def get_is_editable(self, obj):
        return self.check_permission(obj, 'core.change_argument')

    def get_rating(self, obj):
        return ArgumentRatingSerializer(obj, context=self.context).data

    def get_reply_count(self, obj):
        return obj.replies.visible().count()

    def validate_reply_to(self, reply_to):
        return reply_to

    def validate_statement_id(self, statement_id):
        customer = self.context['request'].customer

        try:
            models.Statement.objects.for_customer(customer).get(id=statement_id)
        except models.Statement.DoesNotExist:
            raise exceptions.ValidationError(_("Statement not found"))

        return statement_id

    def get_author(self, instance):
        if instance.created_by:
            serializer = AuthorSerializer(instance.created_by)
            return serializer.data
        return None

    def create(self, validated_data):
        customer = self.context['request'].customer
        user = self.context['request'].user
        statement_id = validated_data['statement']['id']
        del validated_data['statement']

        statement = models.Statement.objects.for_customer(customer).get(
            id=statement_id)

        if not statement.discussion.has_arguments:
            raise exceptions.PermissionDenied(
                _("Arguments are not allowed in this discussion."))

        if 'reply_to' in validated_data and not statement.discussion.has_replies:
            raise exceptions.PermissionDenied(
                _("Replies are not allowed in this discussion."))

        argument = models.Argument.objects.create(
            statement=statement,
            created_by=user,
            **validated_data
        )

        # TODO: add news argument [Blame]
        customer_users = User.objects.filter(customer=customer)
        for customer_user in customer_users:
            if customer_user.id != user.id:
                models.News.objects.create(
                    user=customer_user,
                    discussion=statement.discussion,
                    statement=statement,
                    argument=argument)

        return argument


class UpdateArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Argument
        fields = ('title', 'text', 'is_pro')


class VoteSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=-3, max_value=3)


class BarometerSerializer(NonNullSerializerMixin, serializers.ModelSerializer):
    wording = WordingValueSerializer(
        source='discussion.discussion_wording.words', many=True
    )
    count = serializers.IntegerField(source='barometer_count')
    rating = serializers.FloatField(source='barometer_value')
    user_rating = serializers.SerializerMethodField()
    count_ratings = serializers.SerializerMethodField()

    class Meta:
        model = models.BarometerVote
        fields = ('count', 'rating', 'user_rating', 'count_ratings', 'wording')
        read_only_fields = (
            'count', 'rating', 'user_rating', 'count_ratings', 'wording'
        )

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return None

        try:
            rating = obj.barometer_votes.get(user=user)
        except models.BarometerVote.DoesNotExist:
            return None
        return rating.value

    def get_count_ratings(self, obj):
        ratings = list(obj.barometer_votes.order_by('value').values_list(
            'value', flat=True
        ))
        return {value: ratings.count(value) for value in range(-3, 4)}


class StatementSerializer(NonNullSerializerMixin,
                          serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.display_name', read_only=True)
    discussion_id = serializers.CharField(source='discussion.external_id', required=True)
    statement = serializers.CharField(required=True)
    arguments = serializers.SerializerMethodField()
    barometer = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)
    author = serializers.SerializerMethodField()
    is_deletable = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()
    pdfs = serializers.SerializerMethodField()

    class Meta:
        model = models.Statement
        fields = ('id', 'discussion_id', 'created_by', 'statement', 'description', 'created_at',
                  'arguments', 'barometer', 'is_editable', 'image', 'video',
                  'thumbnail', 'is_deletable', 'status', 'author', 'pdfs', 'copyright_info')
        read_only_fields = ('id', 'created_by', 'created_at', 'discussion_id',
                            'arguments', 'barometer', 'author', 'pdfs')

    def check_permission(self, obj, permission):
        success = True
        request = self.context['request']
        if request.user.is_anonymous:
            success = False
        if not request.user.has_perm(permission):
            if timezone.now() - obj.created_at > timedelta(minutes=30):
                success = False
            if obj.last_related_activity is not None:
                success = False
            if request.user != obj.created_by:
                success = False
        return success

    def get_is_deletable(self, obj):
        return self.check_permission(obj, 'core.delete_statement')

    def get_is_editable(self, obj):
        return self.check_permission(obj, 'core.change_statement')

    def get_pdfs(self, statement):
        pdfs = statement.statement_associated_files.all()
        serializer = AssociatedFileSerializer(pdfs, many=True, context=self.context)
        return serializer.data

    def get_arguments(self, statement):
        arguments = statement.arguments.visible().without_replies()
        serializer = ArgumentSerializer(arguments, many=True, context=self.context)
        return serializer.data

    def get_barometer(self, statement):
        if statement.discussion.has_barometer:
            return BarometerSerializer(statement, context=self.context).data
        return None

    def validate_discussion_id(self, discussion_id):
        customer = self.context['request'].customer

        try:
            models.Discussion.objects.get(
                customer=customer, external_id=discussion_id)
        except models.Discussion.DoesNotExist:
            raise exceptions.ValidationError(_("Discussion not found﻿"))

        return discussion_id

    def create(self, validated_data):
        customer = self.context['request'].customer
        user = self.context['request'].user
        pdfs = self.context['request'].FILES
        discussion_id = validated_data['discussion']['external_id']
        del validated_data['discussion']

        discussion = models.Discussion.objects.get(
            customer=customer, external_id=discussion_id)

        statement = models.Statement.objects.create(
            discussion=discussion,
            created_by=user,
            **validated_data
        )

        print("statement create")
        #TODO: add news statement [Blame 12/28]
        customer_users = User.objects.filter(customer=customer)
        for customer_user in customer_users:
            if customer_user.id != user.id:
                models.News.objects.create(
                    user=customer_user,
                    discussion=discussion,
                    statement=statement)

        # add pdfs
        if pdfs:
            for pdf_key in pdfs:
                pdf = pdfs[pdf_key]
                fs = FileSystemStorage()
                filename = fs.save('private/'+random_string(32)+'_'+pdf.name, pdf)
                models.AssociatedFile.objects.create(
                    statement=statement,
                    filename=filename,
                )

        return statement

    def get_author(self, instance):
        if instance.created_by:
            serializer = AuthorSerializer(instance.created_by)
            return serializer.data
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'video' in ret and ret['video']:
            ret['video'] = YoutubeBackend(ret['video']).get_code()
        return ret


class UpdateStatementSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = models.Statement
        fields = ('statement', 'description', 'image', 'video', 'copyright_info')


class DiscussionListSerializer(PermissionSerializerMixin, serializers.ModelSerializer):
    tags = TagListField()

    class Meta:
        exclude = ('created_at', 'modified_at', 'deleted_at')
        model = models.DiscussionList


class BaseDiscussionSerializer(PermissionSerializerMixin, serializers.Serializer):
    url = serializers.URLField(required=False, source='source_url')
    created_by = serializers.CharField(source='created_by.display_name', read_only=True)
    tags = TagListField(required=False)

    def get_author(self, discussion):
        if discussion.created_by:
            serializer = AuthorSerializer(discussion.created_by)
            return serializer.data
        return None


class ListDiscussionSerializer(NonNullSerializerMixin,
                               BaseDiscussionSerializer,
                               serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    barometer = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    pdfs = serializers.SerializerMethodField()
    discussion_users = serializers.SerializerMethodField()

    class Meta:
        model = models.Discussion
        fields = ('external_id', 'url', 'description', 'created_by', 'created_at', 'image',
                  'last_activity', 'tags', 'multiple_statements_allowed', 'statement',
                  'has_barometer', 'has_arguments', 'has_replies', 'discussion_wording',
                  'user_can_add_replies', 'argument_count', 'statement_count',
                  'is_editable', 'is_deletable', 'barometer', 'start_time',
                  'end_time', 'statements', 'pdfs', 'author', 'discussion_users', 'is_private',
                  'barometer_behavior', 'copyright_info')
        read_only_fields = fields

    def get_barometer(self, discussion):
        if discussion.has_barometer and not discussion.multiple_statements_allowed:
            statement = discussion.statements.first()
            if statement:
                return BarometerSerializer(statement, context=self.context).data
        return None

    def get_pdfs(self, discussion):
        pdfs = discussion.associated_files.all()
        serializer = AssociatedFileSerializer(pdfs, many=True, context=self.context)
        return serializer.data

    def get_discussion_users(self, discussion):
        return discussion.discussion_users.all().values_list('id', flat=True)


class DiscussionSerializer(BaseDiscussionSerializer, serializers.ModelSerializer):
    statements = serializers.SerializerMethodField()
    pdfs = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)
    url = serializers.URLField(required=False, allow_null=True, allow_blank=True, source='source_url')
    external_id = serializers.CharField(required=False, allow_null=True)
    author = serializers.SerializerMethodField()
    users = serializers.ListField(required=False, child=serializers.CharField())
    discussion_users = serializers.SerializerMethodField()
    # NOTE: queryset will be restricted in `get_fields`
    wording = serializers.PrimaryKeyRelatedField(
        queryset=models.Wording.objects.all(),
        required=False, write_only=True,
        source='discussion_wording')

    class Meta:
        model = models.Discussion
        fields = ('external_id', 'created_by', 'created_at',
                  'url', 'description', 'tags',
                  'statement', 'statements', 'wording',
                  'multiple_statements_allowed', 'user_can_add_replies',
                  'has_barometer', 'has_arguments', 'has_replies', 'discussion_wording',
                  'is_editable', 'is_deletable', 'start_time', 'image',
                  'end_time', 'pdfs', 'author', 'is_private', 'users', 'discussion_users',
                  'barometer_behavior', 'copyright_info')
        read_only_fields = ('created_by', 'statements', 'pdfs', 'author', 'discussion_users')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        # PrimaryKeyRelatedField requires a queryset
        # But since we have no access to the customer while constructing,
        # we have to override the queryset here.
        customer = self.context['request'].customer
        qs = models.Wording.objects.for_customer(customer)
        fields['wording'].queryset = qs
        return fields

    def get_discussion_users(self, discussion):
        return discussion.discussion_users.all().values_list('id', flat=True)

    def get_statements(self, discussion):
        statements = discussion.statements.visible()
        serializer = StatementSerializer(statements, many=True, context=self.context)
        return serializer.data

    def get_pdfs(self, discussion):
        pdfs = discussion.associated_files.all()
        serializer = AssociatedFileSerializer(pdfs, many=True, context=self.context)
        return serializer.data

    def validate_external_id(self, external_id):
        customer = self.context['request'].customer

        if external_id:
            external_id = external_id.split("#")[0]
            try:
                existDiscussion = models.Discussion.objects.get(
                    customer=customer, external_id=external_id)
                if existDiscussion:
                    raise exceptions.ValidationError(_("ID is already in use."))
            except models.Discussion.DoesNotExist:
                pass
            except:
                raise exceptions.ValidationError(_("ID is already in use."))
        return external_id

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Validate barometer required
        if attrs['has_barometer'] and not attrs.get('discussion_wording'):
            raise exceptions.ValidationError(_("`Wording` needed for Barometer."))

        # Validate date range
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if not start_time:
            attrs["start_time"] = timezone.now()
            start_time = attrs.get("start_time")
        if start_time and end_time:
            if end_time < start_time:
                raise exceptions.ValidationError(
                    {'start_time': "End time cannot be earlier than start time!"}
                )
        return attrs

    def create(self, validated_data):
        customer = self.context['request'].customer
        user = self.context['request'].user
        tags = []
        if 'tags' in validated_data:
            tags = validated_data['tags']
            del validated_data['tags']
        users = []
        if 'users' in validated_data:
            users = validated_data['users']
            del validated_data['users']
        pdfs = self.context['request'].FILES

        external_id = 'd-' + random_string(size=24)
        if 'external_id' in validated_data:
            if validated_data['external_id']:
                external_id = validated_data['external_id']
            del(validated_data['external_id'])

        #TODO:add undiscussion_ids to the user [Blame 12.13]        
        # cur_users = User.objects.filter(customer=customer)
        # for cur_user in cur_users:
        #     if cur_user.undiscussion_ids is '':
        #         cur_user.undiscussion_ids += external_id
        #     else: 
        #         cur_user.undiscussion_ids += "," + external_id                 
        #     cur_user.save()        

        discussion = models.Discussion.objects.create(
            customer=customer,
            created_by=user,
            external_id=external_id,
            **validated_data
        )

        #TODO: add news discussion [Blame 12/28]
        customer_users = User.objects.filter(customer=customer)
        for customer_user in customer_users:
            if customer_user.id != user.id:
                models.News.objects.create(
                    user=customer_user,
                    discussion=discussion
                )

        # add tags
        for tag in tags:
            discussion.tags.add(tag)

        # add users
        is_private = False
        if 'is_private' in validated_data and validated_data['is_private']:
            is_private = True

        if is_private and customer.are_private_discussions_allowed:
            if user.id not in users:
                users.append(user.id)
            for participant_user_id in users:
                try:
                    user_obj = User.objects.get(pk=participant_user_id, customer=customer)
                    if user_obj:
                        discussion.discussion_users.add(user_obj)
                except User.DoesNotExist:
                    pass

        # create corresponding Statement
        if not discussion.multiple_statements_allowed:
            models.Statement.objects.create(
                discussion=discussion,
                created_by=user,
            )

        # add pdfs
        if pdfs:
            for pdf_key in pdfs:
                pdf = pdfs[pdf_key]
                fs = FileSystemStorage()
                filename = fs.save('private/'+random_string(32)+'_'+pdf.name, pdf)
                models.AssociatedFile.objects.create(
                    discussion=discussion,
                    filename=filename,
                )

        return discussion


class UpdateDiscussionSerializer(serializers.ModelSerializer):
    url = serializers.URLField(required=False, allow_null=True, allow_blank=True, source='source_url')
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tags = TagListField(required=False)
    image = Base64ImageField(required=False)
    users = serializers.ListField(required=False, child=serializers.CharField())

    # TODO limit queryset!
    wording = serializers.PrimaryKeyRelatedField(
        queryset=models.Wording.objects.all(),
        required=False, write_only=True,
        source='discussion_wording')

    class Meta:
        model = models.Discussion
        fields = ('url', 'tags',
                  'statement', 'description', 'wording',
                  'multiple_statements_allowed', 'user_can_add_replies',
                  'has_barometer', 'has_arguments', 'has_replies', 'start_time',
                  'end_time', 'image', 'is_private', 'users',
                  'barometer_behavior', 'copyright_info')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Validate date range
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if start_time and end_time:
            if end_time < start_time:
                raise exceptions.ValidationError(
                    {'start_time': "End time cannot be earlier than start time!"}
                )
        return attrs

    def update(self, instance, validated_data):
        statements = instance.statements
        if validated_data.get('multiple_statements_allowed') \
                and statements.filter(statement='').count() == 1:
            statements.all().delete()
        elif not validated_data.get('multiple_statements_allowed') \
                and statements.count() == 0:
            models.Statement.objects.create(
                discussion=instance, created_by=self.context['request'].user,
            )
        customer = self.context['request'].customer
        user = self.context['request'].user
        users = []
        if 'users' in validated_data:
            users = validated_data['users']
            del validated_data['users']

        instance.discussion_users.clear()
        # add users
        is_private = False
        if 'is_private' in validated_data:
            is_private = validated_data['is_private']
        if is_private:
            if user.id not in users:
                users.append(user.id)
            for participant_user_id in users:
                try:
                    user_obj = User.objects.get(pk=participant_user_id, customer=customer)
                    if user_obj:
                        instance.discussion_users.add(user_obj)
                except User.DoesNotExist:
                    pass
        return super(UpdateDiscussionSerializer, self).update(
            instance, validated_data
        )


class UpdateInfoSerializer(serializers.Serializer):
    external_id = serializers.CharField(required=False)
    date_of_last_fetch = serializers.DateTimeField(required=True)


class FlaggingSerializer(serializers.Serializer):
    ARGUMENT = 'argument'
    STATEMENT = 'statement'
    TYPE_CHOICES = (
        (ARGUMENT, "Argument"),
        (STATEMENT, "Statement"),
    )

    id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        fields = ('id', 'type')

    def validate(self, attrs):
        if attrs['type'] == self.ARGUMENT:
            model = models.Argument
        elif attrs['type'] == self.STATEMENT:
            model = models.Statement
        attrs['model'] = model

        # object should exist
        customer = self.context['request'].customer
        try:
            attrs['to_flag'] = model.objects.for_customer(customer)
            attrs['to_flag'] = attrs['to_flag'].visible().get(id=attrs['id'])
        except model.DoesNotExist:
            raise exceptions.NotFound()

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        flag, _ = models.Flag.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(validated_data['model']),
            object_id=validated_data['id'],
            user=user)

        return flag


class CustomerUserInfoSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUserInfoSettings
        exclude = ('id', 'property_model')


class CustomerSerializer(serializers.ModelSerializer):
    user_info_settings = CustomerUserInfoSettingsSerializer(many=True, source='model_properties')
    data_policy_link = serializers.SerializerMethodField()
    available_wordings = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('language', 'default_back_link', 'default_back_title', 'default_wording', 'default_has_replies',
                  'notification_wording', 'user_info_settings', 'theme', 'displayed_username', 'data_policy_link',
                  'is_private', 'invitations_pending', 'public_customer_name', 'customer_representative_name',
                  'available_wordings', 'are_private_discussions_allowed', 'auto_update_interval_for_admins',
                  'auto_update_interval')

    def get_available_wordings(self, obj):
        available_wordings = obj.available_wordings.all()
        serializer = WordingSerializer(available_wordings, many=True, context=self.context)
        return serializer.data

    def get_data_policy_link(self, obj):
        if obj.data_policy_version:
            return obj.data_policy_version.link
        else:
            return ''


class AssociatedFileSerializer(serializers.ModelSerializer):
    discussion_id = serializers.CharField(required=False)
    statement_id = serializers.CharField(required=False)

    class Meta:
        model = models.AssociatedFile
        fields = ('discussion_id', 'statement_id', 'filename', 'name', 'url', 'id')
        read_only_fields = ('name', 'url', 'id', 'filename')

    def validate_discussion_id(self, discussion_id):
        customer = self.context['request'].customer
        if discussion_id:
            try:
                discussion = models.Discussion.objects.get(
                    customer=customer, external_id=discussion_id)
            except models.Discussion.DoesNotExist:
                raise exceptions.ValidationError(_("Discussion not found﻿"))
            return discussion
        return null

    def validate_statement_id(self, statement_id):
        if statement_id:
            try:
                statement = models.Statement.objects.get(id=statement_id)
            except models.Statement.DoesNotExist:
                raise exceptions.ValidationError(_("Statement not found﻿"))
            return statement
        return null

    def create(self, validated_data):
        pdfFile = self.context['request'].FILES['pdf']
        statement = validated_data.get('statement_id', None)
        discussion = validated_data.get('discussion_id', None)
        # add pdf
        fs = FileSystemStorage()
        filename = fs.save('private/'+random_string(32)+'_'+pdfFile.name, pdfFile)
        pdf = models.AssociatedFile.objects.create(
            discussion=discussion,
            statement=statement,
            filename=filename,
        )

        return pdf


class AuthorSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('display_name', 'image', 'id', 'username')
        read_only_fields = ('display_name', 'image', 'id', 'username')
