from django import forms
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django_countries.fields import CountryField
from meeting.models import Reservation, TimeSlot, ULM, Pilot
from meeting.fields import ListTextWidget
from meeting.widgets import ULMRadioIdWidget


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
                 'ulm', 'time_slot', 'depart_time_slot', 'origin_city',
                 'origin_city_code', 'origin_field', 'fuel_reservation',
                 'flight_plan', 'passanger', 'esthetic_cup', 'to_sell'
                 ]

    def __init__(self, *args, **kwargs):
        pilot = kwargs.pop('pilot')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=pilot)
        aviable = TimeSlot.objects.aviables()
        if self.instance.pk is not None:
            if not aviable.filter(pk=self.instance.time_slot.pk).exists():
                aviable |= TimeSlot.objects.get(pk=self.instance.time_slot.pk)
        self.fields['time_slot'].queryset = aviable


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
                 'username', 'first_name', 'last_name',
                 'email']


class PilotForm(forms.ModelForm):

    class Meta:
        model = Pilot
        fields = [
                 'insurance_company', 'insurance_number',
                 'licence_number',
                 ]
        widgets = {
            'insurance_company': ListTextWidget(
                            data_list=[x[1] for x in Pilot.INSURANCE_CHOICES],
                            name='insurance_company')
        }


class ULMForm(forms.ModelForm):

    class Meta:
        model = ULM
        fields = [
                 'constructor', 'model', 'type', 'imatriculation_country',
                 'imatriculation', 'radio_id']
        widgets = {
            'radio_id': ULMRadioIdWidget,
        }


class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user_form': UserEditForm,
        'pilot_form': PilotForm,
    }


class StaffReservationEditForm(forms.Form):  # TODO a completer
    # user
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    # Pilot
    insurance_number = forms.CharField()
    licence_number = forms.CharField()
    pilot_id = forms.IntegerField(widget=forms.HiddenInput)
    # Reservation
    reservation_id = forms.IntegerField(widget=forms.HiddenInput)
    ulm = forms.ModelChoiceField(queryset=ULM.objects.none())
    time_slot = forms.ModelChoiceField(queryset=TimeSlot.objects.none())
    passanger = forms.BooleanField(required=False)
    flight_plan = forms.BooleanField(required=False)
    esthetic_cup = forms.BooleanField(required=False)
    to_sell = forms.BooleanField(required=False)
    # ULM
    ulm_id = forms.IntegerField(widget=forms.HiddenInput)
    constructor = forms.CharField()
    model = forms.CharField()
    type = forms.ChoiceField(choices=ULM.ULM_TYPE_CHOICE)
    imatriculation_country = CountryField().formfield()
    imatriculation = forms.CharField()  # TODO find max lenght
    radio_id = forms.CharField()  # TODO find max lenght

    def __init__(self, *args, **kwargs):
        reservation = kwargs.pop('reservation')
        super(StaffReservationEditForm, self).__init__(*args, **kwargs)
        # Pilot and User
        pilot = reservation.ulm.pilot
        self.fields['insurance_number'].initial = pilot.insurance_number
        self.fields['licence_number'].initial = pilot.licence_number
        self.fields['pilot_id'].initial = pilot.pk
        self.fields['first_name'].initial = pilot.user.first_name
        self.fields['last_name'].initial = pilot.user.last_name
        self.fields['email'].initial = pilot.user.email
        # Reservation
        self.fields['reservation_id'].initial = reservation.pk
        aviable_time_slot = TimeSlot.objects.aviables()
        if not aviable_time_slot.filter(pk=reservation.time_slot.pk).exists():
            aviable_time_slot |= TimeSlot.objects.get(
                                                pk=reservation.time_slot.pk)
        self.fields['time_slot'].queryset = aviable_time_slot
        self.fields['time_slot'].initial = reservation.time_slot
        self.fields['passanger'].initial = reservation.passanger
        self.fields['flight_plan'].initial = reservation.flight_plan
        self.fields['esthetic_cup'].initial = reservation.esthetic_cup
        self.fields['to_sell'].initial = reservation.to_sell
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=pilot)
        self.fields['ulm'].initial = reservation.ulm
        # ulm
        ulm = reservation.ulm
        self.fields['ulm_id'].initial = ulm.pk
        self.fields['constructor'].initial = ulm.constructor
        self.fields['model'].initial = ulm.model
        self.fields['type'].initial = ulm.type
        self.fields['imatriculation_country'].initial = ulm.imatriculation_country
        self.fields['imatriculation'].initial = ulm.imatriculation
        self.fields['radio_id'].initial = ulm.radio_id

    def save(self):
        data = self.cleaned_data
        pilot = Pilot.objects.get(pk=data['pilot_id'])
        if pilot is not None:
            pilot.insurance_number = data['insurance_number']
            pilot.licence_number = data['licence_number']
            pilot.save()

        user = User.objects.get(pk=pilot.user.pk)
        if user is not None:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.save()

        res = Reservation.objects.get(pk=data['reservation_id'])
        ulm = ULM.objects.get(pk=data['ulm_id'])
        if res is not None:
            res.ulm = ulm
            ts = TimeSlot.objects.get(pk=data['time_slot'].pk)
            res.time_slot = ts
            res.passanger = data['passanger']
            res.flight_plan = data['flight_plan']
            res.esthetic_cup = data['esthetic_cup']
            res.to_sell = data['to_sell']
            res.save()

        if ulm is not None:
            ulm.constructor = data['constructor']
            ulm.model = data['model']
            ulm.type = data['type']
            ulm.imatriculation_country = data['imatriculation_country']
            ulm.imatriculation = data['imatriculation']
            ulm.radio_id = data['radio_id']
            ulm.save()

###############################################################################
# AJAX forms
###############################################################################


class AjaxFuelServedForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["fuel_served"]
