from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from meeting.models import Reservation, TimeSlot


class ReservationFilter(FilterSet):
    ulm__imatriculation = CharFilter(label='Imatriculation')
    ulm__radio_id = CharFilter(label='Radio id')
    ulm__pilot__user__first_name = CharFilter(label='First name', lookup_expr='icontains')
    ulm__pilot__user__last_name = CharFilter(label='Last name', lookup_expr='icontains')
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
