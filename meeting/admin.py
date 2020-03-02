from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field

from meeting.models import Meeting, TimeSlot, Reservation, Pilot, ULM
from meeting.fields import ListTextWidget

from core.models import User as CustomUser


###############################################################################
# CustomFilter
###############################################################################

class ArrivalFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('str_Arrived')

    parameter_name = 'is_arrived'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('str_Yes')),
            ('no', _('str_No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(arrival__isnull=False)
        if self.value() == 'no':
            return queryset.exclude(arrival__isnull=False)
        return queryset

###############################################################################
# PILOT
###############################################################################


@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    readonly_fields = ['modification_date']
    search_fields = ('user__username', 'user__email', 'user__first_name',
                     'user__last_name', 'insurance_company',
                     'insurance_number', 'licence_number', 'phone_number')


###############################################################################
# RESERVATION
###############################################################################

class ReservationResources(resources.ModelResource):
    class Meta:
        model = Reservation
        fields = ('reservation_number', 'meeting',
                  "pilot__user__first_name",
                  'pilot__user__last_name', 'pilot__user__email',
                  "pilot__insurance_company", "pilot__insurance_number",
                  "pilot__licence_number", 'pilot__phone_number',
                  'pilot__street_name', 'pilot__mail_complement',
                  'pilot__city', 'pilot__city_code', 'pilot__country',
                  'ulm__constructor', 'ulm__model', 'ulm__type',
                  'ulm__imatriculation_country', 'ulm__imatriculation',
                  'ulm__radio_id',
                  'time_slot', 'depart_time_slot', 'arrival',
                  'fuel_reservation', 'fuel_served', 'flight_plan',
                  'passanger', 'esthetic_cup', 'for_sale',
                  'fuel_reservation_confirmed', 'creation_date',
                  'modification_date', 'origin_city_code', 'origin_field',
                  'confirmed', 'canceled')

    def dehydrate_time_slot(self, res):
        return str(res.time_slot)

    def dehydrate_depart_time_slot(self, res):
        return str(res.depart_time_slot)


class ReservationAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ('reservation_number', "ulm__radio_id",
                     'pilot__user__email', 'pilot__user__last_name',
                     'pilot__user__first_name', 'pilot__user__username')
    readonly_fields = ('creation_date', 'modification_date')
    list_filter = ['meeting', 'confirmed', 'canceled', ArrivalFilter,]
    list_display = ('reservation_number', "display_pilot", "time_slot", "ulm",
                    'confirmed', 'canceled')
    resource_class = ReservationResources


admin.site.register(Reservation, ReservationAdmin)

###############################################################################
# ULM
###############################################################################


@admin.register(ULM)
class ULMAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = (
        'radio_id', 'pilot', 'imatriculation', 'type', 'constructor', 'model')

###############################################################################
# MEETING
###############################################################################


class TimeSlotInline(admin.TabularInline):
    extra = 0
    model = TimeSlot


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date')
    inlines = [TimeSlotInline]


###############################################################################
# USER
###############################################################################


class PilotInline(admin.StackedInline):
    model = Pilot
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    widgets = {
        'insurance_company': ListTextWidget(
                        data_list=[x[1] for x in Pilot.INSURANCE_CHOICES],
                        name='insurance_company')
    }


class CustomUserAdmin(UserAdmin):
    inlines = (PilotInline, )

    def get_inline_instances(self, request, obj=None):
        return super().get_inline_instances(request, obj)


# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
