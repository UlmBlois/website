from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import csv
import operator

from meeting.models import Meeting, TimeSlot, Reservation, Pilot, ULM
from meeting.fields import ListTextWidget


class ExportCsvMixin:
    export_fields = ()
    _field_name = []

    def get_header(self):
        if len(self.export_fields) > 0:
            return [x.replace('__', '_') for x in self.export_fields]
        else:
            meta = self.model._meta
            return [field.verbose_name for field in
                    meta.get_fields(include_hidden=True)]

    def get_field_names(self):
        if len(self.export_fields) > 0:
            return [x.replace('__', '.') for x in self.export_fields]
        else:
            meta = self.model._meta
            return [field.name for field in
                    meta.get_fields(include_hidden=True)]

    def get_row(self, obj):
        return [operator.attrgetter(field)(obj) for field in
                self.get_field_names()]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(self.get_header())
        for obj in queryset:
            writer.writerow(self.get_row(obj))

        return response

    export_as_csv.short_description = _("str_Export_selected")


@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    readonly_fields = ['modification_date']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('creation_date', 'modification_date')
    list_display = ('reservation_number', "display_pilot", "time_slot", "ulm")
    actions = ["export_as_csv"]
    export_fields = ('reservation_number', 'meeting',
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
        if not obj:
            return list()
        if obj.is_staff:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
