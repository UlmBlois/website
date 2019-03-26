from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from meeting.models import Reservation, TimeSlot, ULM, Pilot
from django.utils.translation import gettext_lazy as _


class ReservationFilter(FilterSet):
    ulm__imatriculation = CharFilter(label=_('Imatriculation'))
    ulm__radio_id = CharFilter(label=_('Radio id'))
    ulm__pilot__user__first_name = CharFilter(label=_('First name'),
                                              lookup_expr='icontains')
    ulm__pilot__user__last_name = CharFilter(label=_('Last name'),
                                             lookup_expr='icontains')
    time_slot = ModelChoiceFilter(queryset=TimeSlot.objects.actives())

    class Meta:
        model = Reservation
        fields = [
                 'reservation_number',
                 'time_slot',
                 'ulm__imatriculation',
                 'ulm__radio_id',
                 'ulm__pilot__user__first_name',
                 'ulm__pilot__user__last_name',
                 'fuel_reservation',
                 'flight_plan',
                 'passanger',
                 'esthetic_cup',
                 'to_sell',
                 ]


class ULMFilter(FilterSet):
    class Meta:
        model = ULM
        fields = {
                'constructor': ['icontains'],
                'model': ['icontains'],
                'type': ['exact'],
                'imatriculation_country': ['exact'],
                'imatriculation': ['exact'],
                'radio_id': ['exact'],
                }


class PilotFilter(FilterSet):
    class Meta:
        model = Pilot
        fields = []
