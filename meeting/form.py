# Django
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Third Party
from betterforms.multiform import MultiModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

# Owned
from meeting.models import Reservation, TimeSlot, ULM, Pilot
from meeting.fields import ListTextWidget
from meeting.widgets import ULMRadioIdWidget


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
                 'ulm', 'time_slot', 'depart_time_slot', 'origin_city',
                 'origin_city_code', 'origin_field', 'fuel_reservation',
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
                Column('origin_city_code',
                       css_class='form-group col-md-4 mb-0'),
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
            Submit('submit', _('Submit')),
        )

    def clean(self):
        cleaned_data = super().clean()
        ts = cleaned_data.get("time_slot")
        dts = cleaned_data.get("depart_time_slot")

        if ts == dts:
            msg = _('Arrival and depart time slot should be different')
            self.add_error('time_slot', msg)
            self.add_error('depart_time_slot', msg)

    def _init_form_fields(self, pilot):
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=pilot)
        aviable = TimeSlot.objects.aviables()
        if self.instance.pk is not None:
            if not aviable.filter(pk=self.instance.time_slot.pk).exists():
                aviable = aviable | TimeSlot.objects.filter(
                    pk=self.instance.time_slot.pk)
            if not aviable.filter(
                    pk=self.instance.depart_time_slot.pk).exists():
                aviable = aviable | TimeSlot.objects.filter(
                    pk=self.instance.depart_time_slot.pk)
        self.fields['time_slot'].queryset = aviable


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
            Submit('submit', _('Submit')),
        )


class PilotForm(forms.ModelForm):

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
            'phone_number': PhoneNumberPrefixWidget()
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
            Submit('submit', _('Submit')),
        )


class ULMForm(forms.ModelForm):

    class Meta:
        model = ULM
        fields = [
                 'constructor', 'model', 'type', 'imatriculation_country',
                 'imatriculation', 'radio_id']
        widgets = {
            'radio_id': ULMRadioIdWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
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
            Field('radio_id', css_class='form-group'),
            Submit('submit', _('Submit')),
        )


class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user_form': UserEditForm,
        'pilot_form': PilotForm,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


###############################################################################
# AJAX forms
###############################################################################


class AjaxFuelServedForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["fuel_served"]
