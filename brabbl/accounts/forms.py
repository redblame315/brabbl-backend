from datetime import datetime

from django import forms
from django.forms import widgets
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from brabbl.accounts.models import Customer
from ckeditor.widgets import CKEditorWidget
User = get_user_model()


class WelcomeForm(forms.Form):
    first_name = forms.CharField(label=_("First Name"), required=False)
    last_name = forms.CharField(label=_("Last Name"), required=False)
    gender = forms.IntegerField(
        label=_("Gender"), required=False, widget=widgets.Select(choices=User.GENDER_LIST)
    )
    year_of_birth = forms.IntegerField(label=_("Year of birth"),
                                       min_value=datetime.now().year-150,
                                       max_value=datetime.now().year,
                                       required=False,
                                       widget=forms.TextInput())
    postcode = forms.CharField(label=_("Postcode"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    bundesland_list = list(User.BUNDESLAND_LIST)
    bundesland = forms.CharField(
        label=_("Bundesland"), required=False, widget=widgets.Select(choices=bundesland_list)
    )
    country = forms.CharField(label=_("Country"), required=False)
    organization = forms.CharField(label=_("Organization"), required=False)
    position = forms.CharField(label=_("Position"), required=False)

    def __init__(self, *args, **kwargs):
        _exclude_fields = kwargs.pop('exclude_fields', [])
        super().__init__(*args, **kwargs)
        for item in self.fields.copy():
            if item not in _exclude_fields:
                self.fields.pop(item)
            elif _exclude_fields[item]:
                self.fields[item].required = True


class CustomerForm(forms.ModelForm):
    email_sign = forms.CharField(widget=CKEditorWidget,
                                 label="Email Sign", help_text=_("Allowed parameters: {{domain}}"))

    class Meta:
        model = Customer
        fields = "__all__"

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()
        default_wording = cleaned_data.get("default_wording")
        available_wordings = cleaned_data.get("available_wordings")

        if default_wording and available_wordings and default_wording not in available_wordings:
            raise forms.ValidationError(_("Default wording should be one of available wordings"))
        return cleaned_data
