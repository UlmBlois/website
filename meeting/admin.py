from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from meeting.models import Meeting, TimeSlot, Reservation, Pilot, ULM

admin.site.register(Pilot)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_number', "display_pilot", "time_slot", "ulm")


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
