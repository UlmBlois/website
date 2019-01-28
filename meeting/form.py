from django import forms
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django_countries.fields import CountryField
from meeting.models import Reservation, TimeSlot, ULM, Pilot


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
                 'ulm', 'time_slot', 'fuel_reservation', 'flight_plan',
                 'passanger', 'esthetic_cup', 'to_sell'
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
                 'insurance_number', 'insurance_file',
                 'licence_number', 'licence_file']


class ULMForm(forms.ModelForm):

    class Meta:
        model = ULM
        fields = [
                 'constructor', 'model', 'imatriculation_country',
                 'imatriculation', 'radio_id']


class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'pilot': PilotForm,
    }


class ReservationEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'pilot': PilotForm,
        'reservation': ReservationForm,
        # 'ulm': ULMForm,
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        args, kwargs = super(ReservationEditMultiForm,
                             self).get_form_args_kwargs(key, args, kwargs)
        if key == 'reservation':
            pilot = self.instances.get('pilot', None)
            kwargs.update({'pilot': pilot})
        return args, kwargs


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
    ulm = forms.ChoiceField()
    time_slot = forms.ChoiceField()
    passanger = forms.BooleanField(required=False)
    flight_plan = forms.BooleanField(required=False)
    esthetic_cup = forms.BooleanField(required=False)
    to_sell = forms.BooleanField(required=False)
    # ULM
    ulm_id = forms.IntegerField(widget=forms.HiddenInput)
    constructor = forms.CharField()
    model = forms.CharField()
    imatriculation_country = CountryField()
    imatriculation = forms.CharField()  # TODO find max lenght
    radio_id = forms.CharField()  # TODO find max lenght

    def __init__(self, *args, **kwargs):
        reservation = kwargs.pop('reservation')
        super(StaffReservationEditForm, self).__init__(*args, **kwargs)
        # Pilot and User
        pilot = reservation.ulm.pilot
        self.fields['insurance_number'] = pilot.insurance_number
        self.fields['licence_number'] = pilot.licence_number
        self.fields['pilot_id'] = pilot.pk
        self.fields['first_name'] = pilot.user.first_name
        self.fields['last_name'] = pilot.user.last_name
        self.fields['email'] = pilot.user.email
        # Reservation
        self.fields['reservation_id'] = reservation.pk
        aviable_time_slot = TimeSlot.objects.aviables()
        if not aviable_time_slot.filter(pk=reservation.time_slot.pk).exists():
            aviable_time_slot |= TimeSlot.objects.get(pk=reservation.time_slot.pk)
        self.fields['time_slot'].queryset = aviable_time_slot
        self.fields['passanger'] = reservation.passanger
        self.fields['flight_plan'] = reservation.flight_plan
        self.fields['esthetic_cup'] = reservation.esthetic_cup
        self.fields['to_sell'] = reservation.to_sell
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=pilot)
        self.fields['ulm'] = reservation.ulm
        # ulm
        ulm = reservation.ulm
        self.fields['ulm_id'] = ulm.pk
        self.fields['constructor'] = ulm.constructor
        self.fields['model'] = ulm.model
        self.fields['imatriculation_country'] = ulm.imatriculation_country
        self.fields['imatriculation'] = ulm.imatriculation
        self.fields['radio_id'] = ulm.radio_id





    def save(self):
        data = self.cleaned_data
        pilot = Pilot.objects.get(pk=data['pilot_id'])
        if pilot is not None:
            pilot.insurance_number = data['insurance_number']
            pilot.licence_number = data['licence_number']

        user = User.objects.get(pk=pilot.user.pk)
        if user is not None:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']

        res = Reservation.objects.get(pk=data['reservation_id'])
        if res is not None:
            res.ulm = ULM.objects.get(pk=data['ulm'])
            res.time_slot = TimeSlot.objects.get(pk=data['time_slot'])
            res.passanger = data['passanger']
            res.flight_plan = data['flight_plan']
            res.esthetic_cup = data['esthetic_cup']
            res.to_sell = data['to_sell']

        ulm = ULM.objects.get(pk=data['ulm_id'])
        if ulm is not None:
            ulm.constructor = data['constructor']
            ulm.model = data['model']
            ulm.imatriculation_country = data['imatriculation_country']
            ulm.immatriculation = data['imatriculation']
            ulm.radio_id = data['radio_id']

###############################################################################
# AJAX forms
###############################################################################

class AjaxFuelServedForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["fuel_served"]
