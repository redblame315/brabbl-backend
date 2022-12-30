from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, views
import json

from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import serializers
from django.conf import settings
from datetime import timedelta, datetime

from brabbl.accounts.models import Customer, EmailGroup, EmailTemplate, User
from django.contrib.auth import get_user_model
from brabbl.utils.serializers import MultipleSerializersViewMixin
from brabbl.utils.language_utils import frontend_interface_messages
from brabbl.utils.string import duplicate_name
from brabbl.utils.news import get_news_info
from brabbl.core.models import Discussion, News

from . import serializers, models, permissions


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.StaffOnlyWritePermission]

    def get_queryset(self):
        return models.Tag.objects.for_customer(self.request.customer)


class WordingViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.WordingSerializer

    def get_queryset(self):
        return models.Wording.objects.for_customer(self.request.customer).order_by('name')


class NotificationWordingViewSet(mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    serializer_class = serializers.NotificationWordingSerializer

    def get_queryset(self):
        notification_wording_pk = 0
        if self.request.customer.notification_wording:
            notification_wording_pk = self.request.customer.notification_wording.pk
        return models.NotificationWording.objects.filter(pk=notification_wording_pk)


class DiscussionListViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [permissions.PrivateOnlyIsAuthenticatePermission,
                          permissions.StaffOnlyWritePermission]
    serializer_class = serializers.DiscussionListSerializer
    queryset = models.DiscussionList.objects.all()
    lookup_field = 'url'

    def get_object(self):
        """
        Gets the discussion by the external id passed in through the `external_id`
        request parameter.
        """
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(
            queryset, url=self.request.GET.get('url'))

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            instance = queryset.get(url=self.request.GET.get('url'))
        except models.DiscussionList.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsNotificationViewSet(viewsets.GenericViewSet):
    def send_message(self, request):
        users = User.objects.all()
        for user in users:
            subject, from_email, to = "New Disussions", settings.DEFAULT_FROM_EMAIL, user.email
            text_content = 'Here you can read new discussion list.'
            html_content = '<h>New Discussions</h>'

            if(user.undiscussion_ids == ''):
                continue

            undiscussion_list = user.undiscussion_ids.split(",")
            for undiscussion in undiscussion_list:
                discussion = Discussion.objects.get(external_id=undiscussion)
                html_content += '<h1>' + discussion.statement + '</h1>'
                if(discussion.description is not None):
                    html_content += '<b>' + discussion.description + '</b>'
                # html_content += '<p>' + discussion.created_at + '</p>'

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return Response(
            {"Send mail successfully"},
            status=status.HTTP_200_OK,
        )

    def list(self, request):
        if(request.user.is_anonymous is True):
            return Response({})

        news_data = get_news_info(request.user)

        return Response(news_data)


class DiscussionViewSet(MultipleSerializersViewMixin,
                        viewsets.ModelViewSet):
    permission_classes = [permissions.PrivateOnlyIsAuthenticatePermission,
                          permissions.StaffOnlyWritePermission]
    serializer_class = serializers.DiscussionSerializer
    list_serializer_class = serializers.ListDiscussionSerializer
    update_serializer_class = serializers.UpdateDiscussionSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        """
        Gets the discussion by the external id passed in through the `external_id`
        request parameter.
        """
        queryset = self.filter_queryset(self.get_queryset())
        external_id = self.request.GET.get('external_id')
        obj = get_object_or_404(
            queryset, external_id=external_id)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        if(self.request.user.is_anonymous is not True):
            user = User.objects.get(pk=self.request.user.id)
            discussion = Discussion.objects.get(external_id=external_id)
            news = News.objects.filter(user=user, discussion=discussion)
            if(news.count() > 0):
                news.delete()
            # self.refresh_undiscussion_ids(user, external_id)
        return obj

    def refresh_undiscussion_ids(self, user, external_id):
        undiscussion_ids = user.undiscussion_ids
        split_ids = undiscussion_ids.split(",")
        user.undiscussion_ids = ''
        for split_id in split_ids:
            if split_id != external_id:
                user.undiscussion_ids += split_id + ','
        user.undiscussion_ids = user.undiscussion_ids[:-1]
        user.save()

    def get_queryset(self):
        if hasattr(self.request, 'user'):
            return models.Discussion.objects.for_customer(self.request.customer).visible(self.request.user)
        else:
            return models.Discussion.objects.for_customer(self.request.customer).visible()

    def partial_update(self, request, pk=None):
        current_multiple = request.data.get('multiple_statements_allowed')
        obj = self.get_object()
        if obj.multiple_statements_allowed and not current_multiple:
            models.Statement.objects.create(
                discussion=obj, created_by=request.user,
            )
        elif not obj.multiple_statements_allowed and current_multiple:
            statements = obj.statements.filter(statement='')
            if statements:
                statements[0].delete()
        return super().partial_update(request, pk=pk)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated,
                            permissions.StaffOnlyWritePermission]
        )
    def reset(self, request, **kwargs):
        obj = self.get_object()
        statements = obj.statements.all()

        for statement in statements:
            models.BarometerVote.objects.filter(statement=statement).delete()
            statement.barometer_count = 0
            statement.barometer_value = 0
            statement.save()
            arguments = statement.arguments.all()
            for argument in arguments:
                models.Rating.objects.filter(argument=argument).delete()
                argument.rating_value = 0
                argument.rating_count = 0
                argument.save()

        return Response(
            {},
            status=status.HTTP_200_OK,
        )


class UpdateInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    View to get updated info for discussion
    """

    def post(self, request, *args, **kwargs):
        """
        Return updated objects, if not updated return empty
        """
        serializer = serializers.UpdateInfoSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        date_of_last_fetch = data['date_of_last_fetch']
        external_id = data['external_id']
        response = {
            'needsUpdate': True,
            'fullUpdate': True
        }
        try:
            discussion = models.Discussion.objects.get(
                customer=self.request.customer, external_id=external_id,
                modified_at__gt=date_of_last_fetch)
        except models.Discussion.DoesNotExist:
            response['needsUpdate'] = False
            return Response(response)
        return Response(response)


class StatementViewSet(MultipleSerializersViewMixin,
                       viewsets.ModelViewSet):
    permission_classes = [permissions.PrivateOnlyIsAuthenticatePermission,
                          IsAuthenticatedOrReadOnly,
                          permissions.OwnershipObjectPermission]
    serializer_class = serializers.StatementSerializer
    update_serializer_class = serializers.UpdateStatementSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return models.Statement.objects.for_customer(self.request.customer).visible()

    def perform_create(self, serializer):
        # we need to verify that it is allowed to create a new statement
        external_id = serializer.validated_data['discussion']['external_id']
        discussion = models.Discussion.objects.get(
            customer=self.request.customer, external_id=external_id)
        # check that only staff can add suggestions if user_can_add_replies is False
        if not discussion.multiple_statements_allowed:
            raise PermissionDenied()
        if not discussion.user_can_add_replies:
            if not (self.request.user.is_active and self.request.user.has_perm('core.add_statement')):
                raise PermissionDenied()
        super().perform_create(serializer)

    def perform_destroy(self, instance):
        if (not self.request.user.has_perm('core.delete_statement') and
                timezone.now() - instance.created_at > timedelta(minutes=30)):
            raise PermissionDenied()
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        if (not self.request.user.has_perm('core.change_statement') and
                timezone.now() - instance.created_at > timedelta(minutes=30)):
            raise PermissionDenied()
        super().perform_update(serializer)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.PrivateOnlyIsAuthenticatePermission,
                            IsAuthenticatedOrReadOnly]
        )
    def vote(self, request, **kwargs):
        serializer = serializers.VoteSerializer(
            data=request.data,
            context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        statement = self.get_object()
        if not statement.discussion.has_barometer:
            raise PermissionDenied(_("Discussion has no barometer."))

        user = request.user

        try:
            vote = statement.barometer_votes.get(user=user)
        except models.BarometerVote.DoesNotExist:
            vote = models.BarometerVote.objects.create(
                statement=statement,
                user=user,
                value=serializer.validated_data['rating']
            )

            # TODO: add news vote [Blame 12/28]
            customer_users = User.objects.filter(customer=user.customer)
            for customer_user in customer_users:
                if customer_user.id != user.id:
                    models.News.objects.create(
                        user=customer_user,
                        discussion=statement.discussion,
                        statement=statement,
                        vote=1)
        else:
            vote.value = serializer.validated_data['rating']
            vote.save()

        # refresh current statement
        statement = models.Statement.objects.get(id=statement.id)

        return Response(
            serializers.BarometerSerializer(
                statement, context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.OwnershipObjectPermission]
    )
    def change_status(self, request, **kwargs):
        serializer = serializers.StatusSerializer(
            data=request.data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        statement = self.get_object()
        statement.status = serializer.validated_data['status']
        statement.save()

        return Response(
            {"status": statement.status}, status=status.HTTP_200_OK
        )


class ArgumentViewSet(MultipleSerializersViewMixin,
                      viewsets.ModelViewSet):
    permission_classes = [permissions.PrivateOnlyIsAuthenticatePermission,
                          IsAuthenticatedOrReadOnly,
                          permissions.OwnershipObjectPermission]
    serializer_class = serializers.ArgumentSerializer
    update_serializer_class = serializers.UpdateArgumentSerializer

    def get_queryset(self):
        qs = models.Argument.objects.for_customer(self.request.customer)
        if self.request.method not in ['DELETE', 'PATCH', 'POST']:
            qs = qs.without_replies().visible()
        return qs

    def perform_destroy(self, instance):
        if (not self.request.user.has_perm('core.delete_argument') and
                timezone.now() - instance.created_at > timedelta(minutes=30)):
            raise PermissionDenied()
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        if (not self.request.user.has_perm('core.change_argument') and
                timezone.now() - instance.created_at > timedelta(minutes=30)):
            raise PermissionDenied()
        super().perform_update(serializer)

    @action(methods=['get'], detail=True)
    def replies(self, request, **kwargs):
        argument = self.get_object()
        serializer = serializers.ArgumentSerializer(argument.replies.visible(), many=True,
                                                    context=self.get_serializer_context())
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.PrivateOnlyIsAuthenticatePermission,
                            IsAuthenticatedOrReadOnly]
        )
    def rate(self, request, **kwargs):
        serializer = serializers.RatingSerializer(
            data=request.data,
            context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        argument = self.get_object()
        if not argument.statement.discussion.has_arguments:
            raise PermissionDenied(_("Discussion has no arguments."))

        if argument.status == models.Argument.STATUS_HIDDEN:
            raise ValidationError(_("You can not rate hidden argument"))

        user = request.user

        models.Rating.objects.update_or_create(
            user=user, argument=argument,
            defaults={'value': serializer.validated_data['rating']}
        )

        # refresh current Argument
        argument = models.Argument.objects.get(id=argument.id)

        return Response(
            serializers.ArgumentRatingSerializer(
                argument, context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.OwnershipObjectPermission]
        )
    def change_status(self, request, **kwargs):
        serializer = serializers.StatusSerializer(
            data=request.data,
            context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        argument = self.get_object()
        argument.status = serializer.validated_data['status']
        argument.save()

        return Response(
            {"status": argument.status},
            status=status.HTTP_200_OK,
        )


class FlagAPIView(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    model = models.Flag
    serializer_class = serializers.FlaggingSerializer
    permission_classes = [permissions.PrivateOnlyIsAuthenticatePermission,
                          IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # this method is identical to `CreateModelMixin.create`
        # except for an empty response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TranslationAPIView(APIView):
    """
    View for frontend i18n.
    """

    def get(self, request):
        """
        Return frontend's interface messages with translations.
        """
        return Response(frontend_interface_messages())


class CustomerAPIView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CustomerSerializer
    model = Customer

    def get_object(self):
        """
        Returns customer object
        It is available in request for authenticated frontend application
        """
        return self.request.customer


class CustomerStatisticsAPIView(views.APIView):
    def get(self, request, format=None):
        customer = request.customer

        if not request.user.has_perm('accounts.change_user'):
            raise PermissionDenied(
                _("You do not have permission to users")
            )
        users = get_user_model().objects.filter(customer=customer)
        registeredUserCount = users.count()
        discussionCount = models.Discussion.objects.filter(customer=customer).count()
        statementCount = models.Statement.objects.filter(discussion__customer=customer).count()
        argumentCount = models.Argument.objects.filter(statement__discussion__customer=customer).count()
        barometerVoteCount = models.BarometerVote.objects.filter(statement__discussion__customer=customer).count()
        statistics = {
            "registered_user_count": registeredUserCount,
            "discussion_count": discussionCount,
            "statement_count": statementCount,
            "argument_count": argumentCount,
            "barometer_vote_count": barometerVoteCount,
        }
        return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'statistics': statistics})


class DuplicateObject(View):
    """
    Duplicate Object View. Only staff allowed (see urls config)
    """

    def get(self, request, model, pk):
        """
        Get request.
        :param request: request
        :param model: name of model
        :param pk: pk of duplicated object
        """
        if model == 'wording':
            obj = get_object_or_404(models.Wording, pk=pk)
            words = obj.words.all()
            obj.pk = None
            obj.name = duplicate_name(obj.name)
            obj.save()
            words_copy = []
            for word in words:
                word.pk = None
                word.wording = obj
                words_copy.append(word)
            models.WordingValue.objects.bulk_create(words_copy)
            redirect_url = "/admin/core/wording/%s/"
        elif model == 'notificationwording':
            obj = get_object_or_404(models.NotificationWording, pk=pk)
            messages = obj.model_properties.all()
            markdown_messages = obj.model_markdown_properties.all()
            obj.pk = None
            obj.name = duplicate_name(obj.name)
            obj.save()
            # delete automaticaly added properties
            models.NotificationWordingMessage.objects.filter(property_model=obj.pk).delete()
            models.MarkdownWordingMessage.objects.filter(property_model=obj.pk).delete()
            messages_copy = []
            for message in messages:
                message.pk = None
                message.property_model = obj
                messages_copy.append(message)
            models.NotificationWordingMessage.objects.bulk_create(messages_copy)
            markdown_messages_copy = []
            for message in markdown_messages:
                message.pk = None
                message.property_model = obj
                markdown_messages_copy.append(message)
            models.MarkdownWordingMessage.objects.bulk_create(markdown_messages_copy)
            redirect_url = "/admin/core/notificationwording/%s/"
        elif model == 'emailgroup':
            obj = get_object_or_404(EmailGroup, pk=pk)
            emails = obj.emailtemplate_set.all()
            obj.pk = None
            obj.name = duplicate_name(obj.name)
            obj.save()
            emails_copy = []
            for email in emails:
                email.pk = None
                email.email_group = obj
                emails_copy.append(email)
            EmailTemplate.objects.bulk_create(emails_copy)
            redirect_url = "/admin/accounts/emailgroup/%s/"

        return redirect(redirect_url % obj.pk)


class AssociatedFileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AssociatedFileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        qs = models.AssociatedFile.objects.filter()
        return qs


class MigrateAvailableWordingsForCustomer(View):
    """
    Migrate available wordings for customer.
    check all discussions for customer and add discussion_wording to available_wordings of customer.
    This api is one time needed to setup previous customer's available wordings.
    . Only staff allowed (see urls config)
    """
    def get(self, request):
        redirect_url = "/admin/core/wording/"
        discussions = models.Discussion.objects.visible()
        for discussion in discussions:
            if discussion.discussion_wording and discussion.customer:
                discussion.customer.add_available_wording(discussion.discussion_wording)
        return redirect(redirect_url)
