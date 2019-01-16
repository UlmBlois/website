from django import forms
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
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
        'ulm': ULMForm,
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        args, kwargs = super(ReservationEditMultiForm,
                             self).get_form_args_kwargs(key, args, kwargs)

        print(self.instances.get('pilot', None).pk)
        if key == 'reservation':
            pilot = self.instances.get('pilot', None)
            kwargs.update({'pilot': pilot})
        return args, kwargs
