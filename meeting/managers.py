from django.db import models

import meeting.models as Mod


class MeetingManager(models.Manager):
    def active(self):
        return self.filter(active=True).first()


class TimeSlotManager(models.Manager):
    def actives(self):
        act_meeting = Mod.Meeting.objects.active()
        return self.filter(meeting=act_meeting)

    def aviables(self):
        slots = Mod.TimeSlot.objects.actives()
        selected = []
        for s in slots:
            arrival_count = Mod.Reservation.objects.filter(
                time_slot=s).count()
            depart_count = Mod.Reservation.objects.filter(
                depart_time_slot=s).count()
            if (arrival_count + depart_count) < s.arrivals_slots:
                selected.append(s.pk)
        return self.filter(pk__in=selected)
