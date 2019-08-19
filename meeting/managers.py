from django.db import models

from meeting import models as Mod


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
            if s.arrivals_slots_left() > 0:
                selected.append(s.pk)
        return self.filter(pk__in=selected)


class ReservationManager(models.Manager):
    def actives(self):
        return self.filter(meeting__active=True)

    def unconfirmed_actives(self):
        return self.filter(meeting__active=True,
                           confirmed=False, canceled=False)
