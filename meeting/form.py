from django import forms
from meeting.models import Reservation, TimeSlot, ULM


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
                 'ulm', 'time_slot', 'fuel_reservation', 'flight_plan',
                 'passanger', 'esthetic_cup', 'to_sell'
                 ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['ulm'].queryset = ULM.objects.filter(pilot=user.pilot)
        aviable = TimeSlot.objects.aviables()
        if self.instance.pk is not None:
            if not aviable.filter(pk=self.instance.time_slot.pk).exists():
                aviable |= TimeSlot.objects.get(pk=self.instance.time_slot.pk)
        self.fields['time_slot'].queryset = aviable
