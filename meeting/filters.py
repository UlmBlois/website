from django_filters import FilterSet, CharFilter, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext_lazy as _
from meeting.models import Reservation, TimeSlot, ULM, Pilot
from meeting.fields import ListTextWidget
import logging

logger = logging.getLogger(__name__)


class ReservationFilter(FilterSet):
    ulm__imatriculation = CharFilter(label=_('Imatriculation'),
                                     lookup_expr='icontains')
    ulm__radio_id = CharFilter(label=_('Radio id'), lookup_expr='icontains')
    pilot__user__first_name = CharFilter(label=_('First name'),
                                         lookup_expr='icontains')
    pilot__user__last_name = CharFilter(label=_('Last name'),
                                        lookup_expr='icontains')
    time_slot = ModelChoiceFilter(queryset=TimeSlot.objects.actives())
    fuel_served = BooleanFilter(label=_('Fuel served'),
                                method='filter_numeric_is_set')
    fuel_reservation = BooleanFilter(label=_('Fuel reserved'),
                                     method='filter_numeric_is_set')

    def filter_numeric_is_set(self, queryset, name, value):
        logger.debug('value: %s', str(value))
        if value:
            return queryset.filter(fuel_served__gt=0)
        else:
            return queryset.filter(fuel_served=0)

    class Meta:
        model = Reservation
        fields = [
                 'reservation_number',
                 'time_slot',
                 'ulm__imatriculation',
                 'ulm__radio_id',
                 'pilot__user__first_name',
                 'pilot__user__last_name',
                 'fuel_reservation',
                 'fuel_served',
                 'flight_plan',
                 'passanger',
                 'esthetic_cup',
                 'for_sale',
                 ]


class ULMFilter(FilterSet):
    constructor = CharFilter(label=_('Constructor'), lookup_expr='icontains')
    model = CharFilter(label=_('model'), lookup_expr='icontains')
    radio_id = CharFilter(label=_('Radio id'), lookup_expr='icontains')
    imatriculation = CharFilter(label=_('Imatriculation'),
                                lookup_expr='icontains')

    class Meta:
        model = ULM
        fields = [
                'constructor',
                'model',
                'type',
                'imatriculation_country',
                'imatriculation',
                'radio_id',
                ]


class PilotFilter(FilterSet):
    user__first_name = CharFilter(
        label=_('First name'), lookup_expr='icontains')
    user__last_name = CharFilter(label=_('Last name'),
                                 lookup_expr='icontains')
    insurance_company = CharFilter(label=_('Insurance company'),
                                   lookup_expr='icontains',
                                   widget=ListTextWidget(
                                   data_list=
                                   [x[1] for x in Pilot.INSURANCE_CHOICES],
                                   name='insurance_company'))

    class Meta:
        model = Pilot
        fields = [
                'user__first_name',
                'user__last_name',
                'insurance_company',
                'insurance_number',
                'licence_number',
                ]
