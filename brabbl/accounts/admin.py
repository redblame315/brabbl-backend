from ckeditor.widgets import CKEditorWidget
from django import forms

from django.db import models as db_models
from django.contrib.admin import register, ModelAdmin, StackedInline
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from brabbl.accounts import models
from brabbl.accounts.forms import CustomerForm
from brabbl.utils.admin import SetOfPropertiesInline


class CustomerUserInfoSettingsAdmin(ModelAdmin):
    pass


class CustomerUserInfoSettingsInline(SetOfPropertiesInline):
    model = models.CustomerUserInfoSettings
    fields = ('show_in_signup', 'show_in_profile', 'show_in_welcome', 'is_required')
    verbose_name_plural = _("User Info Settings")

    class Media:
        js = [static("accounts/admin/js/info_settings_checkboxes.js")]


@register(models.Customer)
class CustomerAdmin(ModelAdmin):
    form = CustomerForm
    inlines = [CustomerUserInfoSettingsInline]
    filter_horizontal = ('user_groups', 'available_wordings')


class EmailInline(StackedInline):
    formfield_overrides = {
        db_models.TextField: {'widget': CKEditorWidget},
    }

    class Media:
        js = [static("accounts/admin/js/dynamic_email_type_list.js")]

    model = models.EmailTemplate
    extra = 1
    max_num = 4


@register(models.EmailGroup)
class EmailGroupAdmin(ModelAdmin):
    formfield_overrides = {
        db_models.TextField: {'widget': CKEditorWidget},
    }
    inlines = [EmailInline]


@register(models.UserSocialAuth)
class UserSocialAdmin(ModelAdmin):
    list_display = ('user', 'uid', 'provider', 'customer', 'id')


@register(models.DataPolicy)
class DataPolicyAdmin(ModelAdmin):
    list_display = ('id', 'link', 'version_number', 'title', 'text')


@register(models.DataPolicyAgreement)
class DataPolicyAgreementAdmin(ModelAdmin):
    pass


@register(models.User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'activated_at', 'newsmail_schedule',
    )
    list_filter = ('activated_at', 'customer')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Additional info'), {'fields': (
            'customer', 'image', 'newsmail_schedule', 'last_sent', 'year_of_birth',
            'postcode', 'city', 'country', 'organization', 'position', 'gender', 'bundesland'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_confirmed', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',
                                           'activated_at', 'deleted_at')}),
    )
    readonly_fields = ('activated_at', 'deleted_at', 'last_sent',)
    actions = ['send_newsmail']

    def send_newsmail(self, request, queryset):
        for user in queryset:
            if user.receives_email_notifications:
                user.send_newsmail(force=True)

    send_newsmail.short_description = _("News Email")
