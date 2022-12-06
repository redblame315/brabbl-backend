from rest_framework import exceptions, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from brabbl.utils.serializers import Base64ImageField
from brabbl.utils.http import get_client_ip
from django.utils.timezone import localtime, now
from brabbl.utils.string import random_unique_username, subset_invitations, destruct_invitation, is_valid_email

from brabbl.accounts.models import Customer, EmailGroup, EmailTemplate


class UserAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password')

        if username and password:
            customer = self.context['request'].customer
            customer_username = '{}+{}'.format(username, customer.embed_token)

            user = authenticate(
                customer=customer,
                username=customer_username,
                password=password
            ) or authenticate(
                customer=customer,
                username=username,
                password=password
            )
            if user is None:
                users = get_user_model().objects.filter(
                    customer=customer, email__iexact=username
                )
                if users:
                    user = authenticate(
                        customer=customer,
                        username=users[0].username,
                        password=password
                    )
            if user:
                if not user.is_active:
                    msg = _("This account is inactive.")
                    raise exceptions.ValidationError(msg)
                if customer.is_private and not user.is_confirmed:
                    msg = _("This account is not yet verified")
                    raise exceptions.ValidationError(msg)
            else:
                msg = _("Password or user name is invalid.")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("Username and password must be entered")
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate_password(self, value):
        # TODO
        return value


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(
                customer=self.context['request'].customer,
                email__iexact=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(_("Unknown e-mail."))
        return email


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()  # define to be required
    permissions = serializers.SerializerMethodField()
    image = Base64ImageField()
    linked = serializers.SerializerMethodField()
    unlinked = serializers.SerializerMethodField()
    has_accepted_current_data_policy = serializers.SerializerMethodField()
    participate_discussions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'last_sent',
                   'activated_at', 'deleted_at', 'groups', 'user_permissions']
        read_only_fields = ('id', 'permissions', 'display_name', 'date_joined',
                            'has_accepted_current_data_policy')

    def get_field_names(self, declared_fields, info):
        """
        Hide additional fields during the customer user's info settings
        """
        fields = super().get_field_names(declared_fields, info)
        if self.instance:
            hidden_fields = self.instance.customer.model_properties.filter(
                show_in_profile=False
            ).values_list('key', flat=True)
            if len(hidden_fields) > 0:
                fields = list(set(fields) - set(hidden_fields))
        return fields

    def get_permissions(self, user):
        return Permission.objects.filter(
            Q(user=user) | Q(group__in=user.groups.all())
        ).values_list('codename', flat=True)

    def get_linked(self, user):
        return list(user.custom_social_auth.values_list('provider', 'id', 'uid'))

    def get_unlinked(self, user):
        return list(
            set(['twitter', 'google-oauth2', 'facebook']) - set(
                user.custom_social_auth.values_list('provider', flat=True))
        )

    def get_has_accepted_current_data_policy(self, obj):
        return obj.has_accepted_current_data_policy()

    def get_participate_discussions(self, obj):
        return obj.discussion_user_set.all().values_list('id', flat=True)

    def validate_email(self, value):
        query = get_user_model().objects.all()
        if self.instance:
            # exclude the current user from email duplicate check
            query = query.exclude(pk=self.instance.pk)

        try:
            query.get(
                email__iexact=value, customer=self.context['request'].customer
            )
        except get_user_model().DoesNotExist:
            return value
        except:
            pass

        raise serializers.ValidationError(
            _("This email address is already in use."))

    def validate_username(self, value):
        query = get_user_model().objects.all()
        if self.instance:
            # exclude the current user from email duplicate check
            query = query.exclude(pk=self.instance.pk)

        customer = self.context['request'].customer
        try:
            query.get(
                username__iexact='{}+{}'.format(value, customer.embed_token),
                customer=customer
            )
        except get_user_model().DoesNotExist:
            return value

        raise serializers.ValidationError(_("This username is not available."))

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'username' in ret:
            ret['username'] = ret['username'].rsplit('+', 1)[0]
            ret['display_name'] = instance.display_name
        return ret

    def update(self, instance, validated_data):
        customer = self.context['request'].customer
        for field in validated_data:
            if field == 'username':
                validated_data[field] += '+{}'.format(customer.embed_token)
            if field == 'image' and validated_data['image'].size < 1400:
                continue
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance


class UserCreateSerializer(PasswordSerializer, UserSerializer):
    token = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(UserSerializer.Meta):
        fields = [
            'username', 'first_name', 'last_name', 'email', 'is_confirmed', 'password', 'token',
            'year_of_birth', 'gender', 'country', 'city', 'organization', 'position', 'bundesland'
        ]
        exclude = []

    def validate(self, attrs):
        customer = self.context['request'].customer
        User = self.Meta.model
        opts = User._meta
        # if private discussion validate if already invited
        email = attrs['email']
        email_label = capfirst(opts.get_field('email').verbose_name)
        if customer.is_private:
            if customer.invitations_pending:
                invitations_pending = customer.invitations_pending.splitlines()
                if email not in invitations_pending and email+"-admin" not in invitations_pending:
                    raise serializers.ValidationError(
                        _("{0} is not yet invited.").format(email))
            else:
                raise serializers.ValidationError(
                    _("{0} is not yet invited.").format(email))
        if customer.displayed_username == Customer.DISPLAY_NAME_LAST_NAME:
            if not attrs.get('first_name') or not attrs.get('last_name'):
                raise serializers.ValidationError(
                    {'first_name': _("{0} is required.").format('First Name')}
                )
            if not attrs.get('username'):
                attrs['username'] = random_unique_username()
        else:
            if not attrs.get('username'):
                raise serializers.ValidationError(
                    {'username': _("{0} is required.").format('Username')}
                )
        # validate `unique_together manually to fully customize the error message
        for field_name in ['username', 'email']:
            field_label = capfirst(opts.get_field(field_name).verbose_name)
            if attrs.get(field_name, None):
                if field_name == 'username':
                    attrs[field_name] += '+{}'.format(customer.embed_token)
                try:
                    User.objects.get(**{'customer': customer,
                                        field_name: attrs[field_name]})
                except User.DoesNotExist:
                    pass
                else:
                    raise serializers.ValidationError(
                        _("{0} is already in use.").format(field_label))
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        password = validated_data.pop('password')
        token = validated_data.pop('token', None)

        # add current customer
        validated_data.update({'customer': request.customer})
        validated_data['is_confirmed'] = False
        is_admin = False

        # check if it has invite token then is_confirmed True
        if token:
            invite_info = request.customer.get_info_by_token(token)
            email = validated_data['email']
            if (invite_info and len(invite_info) > 0 and
                    invite_info[0] == email and invite_info[1] == request.customer.id):
                validated_data['is_confirmed'] = True
            if (invite_info and len(invite_info) > 2 and invite_info[2]):
                is_admin = True

        User = get_user_model()
        user = User.objects.create(**validated_data)
        user.set_password(password)
        if is_admin:
            adminGroup = [Group.objects.get(name="Admin")]
            user.groups.set(adminGroup)
        user.save()

        # if customer is private remove email from invitation
        customer = request.customer
        if customer.invitations_pending:
            invitations = customer.invitations_pending.splitlines()

            updatedInvitations = subset_invitations(invitations, [user.email])
            invitations_pending = "\n".join(updatedInvitations)
            customer.invitations_pending = invitations_pending
            customer.save()
        verification_url = request.META.get('HTTP_REFERER')
        if customer.default_back_link:
            verification_url = customer.default_back_link
        if validated_data['is_confirmed'] is False:
            user.send_verification_mail(
                request.customer,
                source_url=verification_url
            )

        if not user.has_accepted_current_data_policy():
            if customer.data_policy_version:
                user.datapolicyagreements.create(
                    user=user,
                    data_policy=customer.data_policy_version,
                    ip_address=get_client_ip(request),
                    date_accepted=localtime(now())
                )
        return user


class UserTokenIdentifierSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        User = get_user_model()
        token = attrs['token']

        try:
            attrs['user'] = User.objects.user_from_token(token)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                _("Auth token is not valid."))
        return attrs


class FormToSerializerBooleanField(serializers.BooleanField):
    TRUE_VALUES = set(('t', 'T', 'true', 'True', 'TRUE', '1', 1, True, 'On', 'on', 'ON'))
    FALSE_VALUES = set(('f', 'F', 'false', 'False', 'FALSE', '0', 0, 0.0, False, 'Off', 'off', 'OFF'))


class UserListSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('display_name', 'image', 'id', 'username', 'email', 'date_joined',
                  'gender', 'position', 'year_of_birth', 'postcode', 'city', 'country',
                  'organization')
        read_only_fields = fields


class UserListUpdateSerializer(serializers.Serializer):
    group = serializers.IntegerField(allow_null=True)
    is_active = FormToSerializerBooleanField()
    user_id = serializers.IntegerField()

    def validate(self, attrs):
        if 'group' in attrs and attrs['group']:
            try:
                attrs['group'] = [Group.objects.get(pk=int(attrs['group']))]
            except Group.DoesNotExist:
                raise serializers.ValidationError(
                    _("Group doesn't exist."))
        else:
            attrs['group'] = []
        return attrs


class InviteParticipantSerializer(serializers.ModelSerializer):
    invitations_pending = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('is_private', 'invitations_pending')

    def get_invitations_pending(self, obj):
        if obj.invitations_pending:
            return sorted(obj.invitations_pending.splitlines())
        return []


class InviteParticipantUpdateSerializer(serializers.Serializer):
    invitations = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        if 'invitations' in attrs and attrs['invitations']:
            invitations = attrs['invitations']
            request = self.context['request']
            is_admin_allow = request.user.is_staff
            for invitation in invitations:
                invitation_obj = destruct_invitation(invitation)
                if not is_admin_allow and invitation_obj["is_admin"]:
                    raise serializers.ValidationError(
                        _("Admin invitation is not allowed"))
                    attrs['invitations'] = []
                if not is_valid_email(invitation_obj["email"]):
                    raise serializers.ValidationError(
                        _("Email is not valid"))
                    attrs['invitations'] = []
            attrs['invitations'] = invitations
        else:
            attrs['invitations'] = []
        return attrs
