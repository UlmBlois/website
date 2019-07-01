# Django
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms.models import modelformset_factory
# Python
import logging

# Third Party
from betterforms.multiform import MultiModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Submit, Row, Column,
                                 Field, MultiWidgetField, HTML, Div)

# Owned
from meeting.models import Reservation, TimeSlot, ULM, Pilot
from meeting.fields import ListTextWidget
from radio_call_sign_field.widgets import CallSingPrefixWidget

logger = logging.getLogger(__name__)


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
                 'ulm', 'time_slot', 'depart_time_slot', 'origin_city',
                 'origin_field', 'fuel_reservation',
                 'flight_plan', 'passanger', 'esthetic_cup', 'for_sale'
                 ]

    def __init__(self, *args, **kwargs):
        pilot = kwargs.pop('pilot')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self._init_form_fields(pilot)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('ulm', css_class='form-group'),
            Row(
                Column('time_slot', css_class='form-group col-md-6 mb-0'),
                Column('depart_time_slot',
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('origin_city', css_class='from-group col-md-4 mb-0'),
                Column('origin_field', css_class='from-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Field('fuel_reservation', css_class='form-group'),
            Row(
                Column('flight_plan', css_class='from-group col-md-3 mb-0'),
                Column('passanger', css_class='from-group col-md-3 mb-0'),
                Column('esthetic_cup', css_class='from-group col-md-3 mb-0'),
                Column('for_sale', css_class='from-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('str_Submit')),
        )

    def clean(self):
        cleaned_data = super().clean()
        ts = cleaned_data.get("time_slot")
        dts = cleaned_data.get("depart_time_slot")

        if ts == dts:
            msg = _('str_Error_Arrival_Depart_Timeslot_Equals')
            self.add_error('time_slot', msg)
            self.add_error('depart_time_slot', msg)

        if dts.start_date < ts.start_date:
            msg = _('str_Error_Depart_Timeslot_Anterior_To_Arrival')
            self.add_error('time_slot', msg)
            self.add_error('depart_time_slot', msg)
        return self.cleaned_data

    def _init_form_fields(self, pilot):
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=pilot)
        aviable = TimeSlot.objects.aviables()
        if self.instance.pk is not None and not self.instance.canceled:
            if not aviable.filter(pk=self.instance.time_slot.pk).exists():
                aviable = aviable | TimeSlot.objects.filter(
                    pk=self.instance.time_slot.pk)
            if not aviable.filter(
                    pk=self.instance.depart_time_slot.pk).exists():
                aviable = aviable | TimeSlot.objects.filter(
                    pk=self.instance.depart_time_slot.pk)
        self.fields['time_slot'].queryset = aviable
        self.fields['depart_time_slot'].queryset = aviable


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
                 'username', 'first_name', 'last_name',
                 'email']

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
            Submit('submit', _('str_Submit')),
        )


class PilotForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(),
        label=_('str_phonenumber'),
        help_text=_('str_helptext_phonenumber')
    )

    class Meta:
        model = Pilot
        fields = [
                 'insurance_company', 'insurance_number',
                 'licence_number', 'phone_number'
                 ]
        widgets = {
            'insurance_company': ListTextWidget(
                            data_list=[x[1] for x in Pilot.INSURANCE_CHOICES],
                            name='insurance_company'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('insurance_company',
                       css_class='form-group col-md-6 mb-0'),
                Column('insurance_number',
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('licence_number', css_class='form-group'),
            Field('phone_number', css_class='form-group'),
            Submit('submit', _('str_Submit')),
        )


class ULMFormSetHelper(FormHelper):
    card_header = "{%% load i18n %%}{%% if forloop.revcounter == 1 %%}%(new)s{%% else %%}%(ulm)s {{ forloop.counter }}{%% endif %%}"
    card_data = {'new': _('str_Add_new'),
                 'ulm': _('str_ULM')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(
                Div(  # TODO add str_Add_new_ulm to po files
                    HTML(self.card_header % self.card_data),
                    css_class="card-header",
                    ),
                Div(
                    Field('type', css_class='form-group'),
                    Row(
                        Column('constructor', css_class='form-group col-md-6 mb-0'),
                        Column('model', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('imatriculation_country',
                               css_class='form-group col-md-6 mb-0'),
                        Column('imatriculation', css_class='from-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        MultiWidgetField('radio_id', css_class='form-group',
                                         attrs=({'class': 'form-control'},
                                                {'class': 'form-control'}),
                                         template="radio_call_sign_crispy_field.html"),
                        css_class='form-row'
                    ),
                    css_class="card-body"
                ),
                css_class='card',
            ),

        )
        self.render_required_fields = True
        self.add_input(Submit('submit', _('str_Submit')))


class BaseULMForm(forms.ModelForm):

    class Meta:
        model = ULM
        fields = [
                 'constructor', 'model', 'type', 'imatriculation_country',
                 'imatriculation', 'radio_id']
        widgets = {
            'radio_id': CallSingPrefixWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = ULMFormSetHelper()


class ULMForm(BaseULMForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UlmFormSet = modelformset_factory(ULM, BaseULMForm,
                                  widgets={'radio_id': CallSingPrefixWidget})


class UserEditMultiForm(MultiModelForm):
    # We have to set base_fields to a dictionary because the WizardView
    # tries to introspect it.
    base_fields = {}
    form_classes = {
        'user_form': UserEditForm,
        'pilot_form': PilotForm,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('str_Submit')))


###############################################################################
# AJAX forms
###############################################################################


class AjaxFuelServedForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["fuel_served"]
