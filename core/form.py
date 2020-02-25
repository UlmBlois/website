# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
# Third party
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
# Owned
# from core.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('str_First_name'),
                                 max_length=30,
                                 required=False)
    last_name = forms.CharField(label=_('str_Last_name'),
                                max_length=30,
                                required=False)
    email = forms.EmailField(label=_('str_Email'), max_length=254)

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-group'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('email', css_class='form-group'),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='from-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('str_Register')),
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (username and get_user_model().objects.filter(username__iexact=username).exists()):
            raise forms.ValidationError(
                _('str_Username_already_used'),
                code='username_already_used',
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(username__iexact=email).exists():
            raise forms.ValidationError(
                _('str_Email_already_used'),
                code='email_already_used',
            )
        return email


class PasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('str_Submit'), css_class='btn-primary'))
