from brabbl.accounts.authentication import BrabblIFrameTokenAuthentication
from django.core.validators import URLValidator
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import generics, views, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated, ValidationError, PermissionDenied
from rest_framework.response import Response
from social_django.utils import load_strategy

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
import pkg_resources

from brabbl.accounts import serializers
from brabbl.accounts.forms import WelcomeForm
from brabbl.accounts.models import Customer
from brabbl.accounts.social import partial_load
from brabbl.core.models import MarkdownWordingMessage, User
from brabbl.core.permissions import IsAuthenticated
from brabbl.utils import language_utils
from brabbl.utils.http import get_next_url
from brabbl.utils.models import delete_all_unexpired_sessions_for_user
from brabbl.utils import mail
from brabbl.utils.string import duplicate_name, subset_invitations
from django.conf import settings


class WelcomeView(FormView):
    template_name = 'accounts/welcome.html'
    form_class = WelcomeForm
    customer_token = None

    def get(self, *args, **kwargs):
        if self.request.GET.get('cancel') is not None:
            return self.complete_redirect()
        return super().get(*args, **kwargs)

    def complete_redirect(self):
        user = self.get_token_user()
        if user:
            user.activate()
            user.confirm()
            next_url = self.request.GET.get('next')
            val = URLValidator()
            try:
                val(next_url)
            except ValidationError:
                if user:
                    next_url = user.customer.allowed_domains.splitlines()[0]
            return redirect(next_url)

        self.get_customer(user)
        self.request.session.modified = True
        partial_token = self.request.session.get('partial_pipeline_token')
        strategy = load_strategy(self.request)
        strategy.session_set('user_created', True)
        backend = partial_load(strategy, partial_token, self.customer_token).backend
        return redirect('social:complete', backend=backend)

    def get_customer(self, user=None):
        if not user:
            user = self.get_token_user()
        if user:
            return user.customer
        self.customer_token = self.request.session.get('customer_token', '')
        return get_object_or_404(Customer, embed_token=self.customer_token)

    def get_context_data(self, *args, **kwargs):
        user = self.get_token_user()
        customer = self.get_customer(user)
        # set language for user by customer
        self.request = language_utils.set_language(
            self.request, customer.language
        )
        context = super().get_context_data(*args, **kwargs)
        context['wording'] = {
            'welcome_title': _("Welcome"),
            'welcome_text': _(
                """By signing up, you agree to %s Basic Rules, Terms of Service, and Privacy Policy.<br/>
        Have fun discussing on customer page. This text should be customizable.<br/>
        Please update the following required fields"""
            ) % customer.name
        }
        if self.kwargs.get('token'):
            context['wording']['welcome_text'] = _(
                """Thank you very much. Your brabbl account at {}
                has been successfully activated."""
            ).format(customer.domain)
        if customer.notification_wording:
            wordings = MarkdownWordingMessage.objects.filter(
                property_model__pk=customer.notification_wording.pk,
                key__in=['welcome_title', 'welcome_text_email', 'welcome_text_social']
            )
            for wording in wordings:
                if wording.key == 'welcome_title':
                    if wording.value:
                        context['wording']['welcome_title'] = wording.value
                if self.kwargs.get('token'):
                    if wording.key == 'welcome_text_email':
                        if wording.value:
                            context['wording']['welcome_text'] = wording.value
                else:
                    if wording.key == 'welcome_text_social':
                        if wording.value:
                            context['wording']['welcome_text'] = wording.value
        context['CUSTOMER_THEME'] = customer.theme

        return context

    def get_user(self):
        self.get_customer()
        partial_token = self.request.session.get('partial_pipeline_token')
        strategy = load_strategy(self.request)
        partial_pipeline = partial_load(strategy, partial_token, self.customer_token)
        try:
            pk = partial_pipeline.kwargs.get('user', None).pk
        except AttributeError:
            pk = None
        return get_user_model().objects.filter(id=pk)

    def get_token_user(self):
        User = get_user_model()
        token = self.kwargs.get('token')
        if not token:
            return None
        try:
            return User.objects.get_by_token(self.kwargs.get('token'))
        except User.DoesNotExist:
            return None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        result = {}
        user = self.get_user().values()
        if user and user[0]:
            result = user[0]
        else:
            user = self.get_token_user()
            if user:
                result = user.__dict__
        return result

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        customer = self.get_customer()
        kwargs['exclude_fields'] = dict(customer.model_properties.filter(
            show_in_welcome=True
        ).values_list('key', 'is_required'))
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            user = self.get_token_user()
            if user:
                for item in form.cleaned_data:
                    setattr(user, item, form.cleaned_data[item])
                user.save()
            else:
                self.get_user().update(**form.cleaned_data)
        return self.complete_redirect()


class UserLoginAPIView(views.APIView):
    def post(self, request):
        serializer = serializers.UserAuthTokenSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'has_accepted_current_data_policy': user.has_accepted_current_data_policy()
        })


class UserLogoutAPIView(views.APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            delete_all_unexpired_sessions_for_user(user=self.request.user)
            logout(self.request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        if self.request.user and self.request.user.is_authenticated:
            return self.request.user
        raise NotAuthenticated()


class UserCreateAPIView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserCreateSerializer


class PasswordResetAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserEmailSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        UserModel = get_user_model()
        user = UserModel._default_manager.get(customer=request.customer, email__iexact=serializer.data['email'],
                                              is_active=True)

        user.send_password_reset_mail(request.customer,
                                      source_url=request.META.get('HTTP_REFERER'))
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmDataPolicyView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        if not request.user.has_accepted_current_data_policy():
            if request.user.customer.data_policy_version:
                request.user.datapolicyagreements.create(
                    user=request.user,
                    data_policy=request.user.customer.data_policy_version,
                    ip_address=get_client_ip(request),
                    date_accepted=localtime(now())
                )
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetView(FormView):
    template_name = 'accounts/password_reset.html'
    form_class = SetPasswordForm

    def get_user(self):
        User = get_user_model()
        token = self.kwargs.get('token', None)

        try:
            return User.objects.get_by_token(token)
        except User.DoesNotExist:
            return None

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.get_user(), **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        user = self.get_user()
        theme = Customer.THEME_BRABBL
        if user:
            # set language for user by customer
            self.request = language_utils.set_language(
                self.request, user.customer.language
            )
            theme = user.customer.theme
        # add redirect url to context
        next_url = get_next_url(self.request.GET.get('next', ''), user)

        context.update({
            'user': user,
            'next': next_url,
            'CUSTOMER_THEME': theme
        })
        return context

    def form_valid(self, form):
        form.save()
        context = self.get_context_data(form=form)
        context.update({'success': True})
        return self.render_to_response(context)


class UserListView(TemplateView):
    template_name = 'accounts/user_list.html'

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

    def get_object(self):
        result = BrabblIFrameTokenAuthentication().authenticate(self.request)
        if result:
            return result
        else:
            raise NotAuthenticated

    def get_context_data(self, **kwargs):
        user = self.get_object()
        users = get_user_model().objects.filter(customer=user.customer).prefetch_related('groups').order_by(
            '-date_joined')
        # set language for user by customer
        self.request = language_utils.set_language(
            self.request, user.customer.language
        )
        context = super(UserListView, self).get_context_data(**kwargs)
        context['customer'] = user.customer
        context['groups'] = user.customer.user_groups.all()
        context['users'] = users
        context['allowed_domains'] = ",".join(user.customer.allowed_domains.splitlines())
        context['additional_info'] = user.customer.model_properties.filter(show_in_profile=True)
        context['user_token'] = Token.objects.get(user=user).key
        context['display_fullname'] = user.customer.displayed_username == Customer.DISPLAY_NAME_LAST_NAME
        context['CUSTOMER_THEME'] = user.customer.theme
        return context


class UserListAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customer = request.customer
        users = get_user_model().objects.filter(customer=customer)
        resp_users = []
        if not request.user.has_perm('accounts.change_user'):
            raise PermissionDenied(
                _("You do not have permission to users")
            )
        for u in users:
            serializer = serializers.UserListSerializer(u)
            resp_users.append(serializer.data)
        return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'users': resp_users})

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserListUpdateSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        User = get_user_model()
        try:
            user = User.objects.get(pk=data['user_id'])
        except User.DoesNotExist:
            raise ValidationError(
                _("User doesn't exist."))
        if not self.request.user.has_perm('accounts.change_user') or request.user.customer != user.customer:
            raise PermissionDenied(
                _("You do not have permission to change this user.")
            )
        user.is_active = data['is_active']
        user.groups.set(data['group'])
        user.save()
        return Response(status=status.HTTP_200_OK, data={'status': 'OK'})


class InviteParticipantAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customer = request.customer
        serializer = serializers.InviteParticipantSerializer(customer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        customer = request.customer
        serializer = serializers.InviteParticipantUpdateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        invitations = serializer.validated_data["invitations"]

        # exclude emails already signed up
        query = User.objects.filter(customer=customer, email__isnull=False)
        users = query.exclude(email__exact='').all().values('email')
        emails = []
        for u in users:
            emails.append(u["email"])

        newInvitations = subset_invitations(invitations, emails)
        alreadySignupInvitations = list(set(invitations)-set(newInvitations))

        # exclude emails already in invitations_pending
        inviteParticipantSerializer = serializers.InviteParticipantSerializer(customer)
        currentInvitations = inviteParticipantSerializer.data["invitations_pending"]
        newInvitations = subset_invitations(newInvitations, currentInvitations)

        # send invitation to extracted emails
        customer.send_invitations(newInvitations, customer.default_back_link)

        updatedInvitations = currentInvitations+newInvitations
        invitations_pending = "\n".join(updatedInvitations)
        customer.invitations_pending = invitations_pending
        customer.save()
        return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'invitations': newInvitations,
                                                         'already_signup_invitations': alreadySignupInvitations})

    def patch(self, request, *args, **kwargs):
        customer = request.customer
        serializer = serializers.InviteParticipantUpdateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        invitations = serializer.validated_data["invitations"]

        inviteParticipantSerializer = serializers.InviteParticipantSerializer(customer)
        currentInvitations = inviteParticipantSerializer.data["invitations_pending"]

        updatedInvitations = list(set(currentInvitations)-set(invitations))
        invitations_pending = "\n".join(updatedInvitations)
        customer.invitations_pending = invitations_pending
        customer.save()
        return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'invitations': updatedInvitations})


class AccountDuplicateObject(View):
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
        if model == 'customer':
            obj = get_object_or_404(Customer, pk=pk)
            user_groups = obj.user_groups.all()
            available_wordings = obj.available_wordings.all()
            obj.duplicate()
            obj.user_groups.set(user_groups)
            obj.available_wordings.set(available_wordings)
            redirect_url = "/admin/accounts/customer/%s/"

        return redirect(redirect_url % obj.pk)


class VersionApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        version = settings.VERSION
        return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'version': version})
