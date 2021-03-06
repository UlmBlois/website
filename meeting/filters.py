from django_filters import FilterSet, CharFilter, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext_lazy as _
from meeting import models
from meeting.fields import ListTextWidget
import logging

logger = logging.getLogger(__name__)


class ReservationFilter(FilterSet):
    ulm__imatriculation = CharFilter(label=_('str_Imatriculation'),
                                     lookup_expr='icontains')
    ulm__radio_id = CharFilter(label=_('str_Aircraft_registration_number'),
                               lookup_expr='icontains')
    pilot__user__first_name = CharFilter(label=_('str_First_name'),
                                         lookup_expr='icontains')
    pilot__user__last_name = CharFilter(label=_('str_Last_name'),
                                        lookup_expr='icontains')
    time_slot = ModelChoiceFilter(
        queryset=lambda req: models.TimeSlot.objects.actives())
    fuel_served = BooleanFilter(label=_('str_Fuel_served'),
                                method='filter_numeric_is_set')
    fuel_reservation = BooleanFilter(label=_('str_Fuel_reserved'),
                                     method='filter_numeric_is_set')

    def filter_numeric_is_set(self, queryset, name, value):
        if value:
            lookup = '__'.join([name, 'gt'])
            return queryset.filter(**{lookup: 0})
        else:
            return queryset.filter(**{name: 0})

    class Meta:
        model = models.Reservation
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
    constructor = CharFilter(label=_('str_Constructor'),
                             lookup_expr='icontains')
    # Translators: aircraft model
    model = CharFilter(label=_('str_Model'), lookup_expr='icontains')
    radio_id = CharFilter(label=_('str_Aircraft_registration_number'),
                          lookup_expr='icontains')
    imatriculation = CharFilter(label=_('str_Imatriculation'),
                                lookup_expr='icontains')

    class Meta:
        model = models.ULM
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
        label=_('str_First_name'), lookup_expr='icontains')
    user__last_name = CharFilter(label=_('str_Last_name'),
                                 lookup_expr='icontains')
    insurance_company = CharFilter(
        label=_('str_Insurance_company'),
        lookup_expr='icontains',
        widget=ListTextWidget(
            data_list=[x[1] for x in models.Pilot.INSURANCE_CHOICES],
            name='insurance_company'))

    class Meta:
        model = models.Pilot
        fields = [
                'user__first_name',
                'user__last_name',
                'insurance_company',
                'insurance_number',
                'licence_number',
                ]
