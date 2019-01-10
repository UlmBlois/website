from django_filters import FilterSet
from meeting.models import Reservation


class ReservationFilter(FilterSet):
    class Meta:
        model = Reservation
        fields = [
                 'reservation_number', 'time_slot', 'fuel_reservation',
                 'flight_plan', 'passanger', 'esthetic_cup', 'to_sell']
