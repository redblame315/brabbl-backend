from brabbl.core.models import Discussion, Wording, Statement
from brabbl.accounts.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class DiscussionForm(forms.ModelForm):

    description = forms.CharField(required=False, widget=forms.Textarea,
                                  max_length=1024, label="Description (optional)")

    def __init__(self, *args, **kwargs):
        _newly_created = kwargs.get('instance') is None
        super(DiscussionForm, self).__init__(*args, **kwargs)

        if not _newly_created:
            self.fields['created_by'].queryset = User.objects.filter(customer=self.instance.customer)

    class Meta:
        model = Discussion
        fields = "__all__"

    def clean(self):
        cleaned_data = super(DiscussionForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time < start_time:
                raise forms.ValidationError(_("End time cannot be earlier than start time!"))
        return cleaned_data


class WordingForm(forms.ModelForm):

    description = forms.CharField(required=False, widget=forms.Textarea,
                                  max_length=1024, label="Description (optional)")

    class Meta:
        model = Wording
        fields = "__all__"


class StatementForm(forms.ModelForm):

    description = forms.CharField(required=False, widget=forms.Textarea,
                                  max_length=1024, label="Description (optional)")

    def __init__(self, *args, **kwargs):
        _newly_created = kwargs.get('instance') is None
        super(StatementForm, self).__init__(*args, **kwargs)
        if not _newly_created:
            self.fields['created_by'].queryset = User.objects.filter(customer=self.instance.discussion.customer)

    class Meta:
        model = Statement
        fields = "__all__"


class ArgumentForm(forms.ModelForm):

    original_title = forms.CharField(required=False, widget=forms.TextInput,
                                     max_length=1024, label="Original title (optional)")
    original_text = forms.CharField(required=False, widget=forms.Textarea,
                                    label="Original text (optional)")

    def __init__(self, *args, **kwargs):
        _newly_created = kwargs.get('instance') is None
        super(ArgumentForm, self).__init__(*args, **kwargs)
        if not _newly_created:
            self.fields['created_by'].queryset = User.objects.filter(customer=self.instance.discussion.customer)

    class Meta:
        model = Statement
        fields = "__all__"


class DiscussionListForm(forms.ModelForm):

    url = forms.CharField(required=False, widget=forms.TextInput,
                          max_length=1024, label="URL (optional)")

    class Meta:
        model = Statement
        fields = "__all__"
