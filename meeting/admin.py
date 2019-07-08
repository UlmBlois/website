from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ExportMixin

from meeting.models import Meeting, TimeSlot, Reservation, Pilot, ULM
from meeting.fields import ListTextWidget


@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    readonly_fields = ['modification_date']


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
                  'modification_date', 'origin_city', 'origin_field',
                  'confirmed', 'canceled')


class ReservationAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['meeting']
    readonly_fields = ('creation_date', 'modification_date')
    list_display = ('reservation_number', "display_pilot", "time_slot", "ulm")
    resource_class = ReservationResources


admin.site.register(Reservation, ReservationAdmin)


class TimeSlotInline(admin.TabularInline):
    extra = 0
    model = TimeSlot


@admin.register(ULM)
class ULMAdmin(admin.ModelAdmin):
    list_display = (
        'radio_id', 'pilot', 'imatriculation', 'constructor', 'model')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date')
    inlines = [TimeSlotInline]


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
        if not obj or obj.is_staff:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
