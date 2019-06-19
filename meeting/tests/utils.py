from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta
from meeting.models import Meeting, TimeSlot, Pilot, Reservation, ULM


def create_meeting(name, start_date, active):
    end_date = start_date + timedelta(days=2)
    registration_start = start_date - timedelta(days=60)
    registration_end = start_date - timedelta(days=5)
    return Meeting.objects.create(
            name=name,
            active=active,
            start_date=start_date,
            end_date=end_date,
            registration_start=registration_start,
            registration_end=registration_end)


def create_time_slot(meeting, start_date, arrivals_slots, end_date=None):
    if end_date is None:
        end_date = start_date + timedelta(minutes=30)
    return TimeSlot.objects.create(meeting=meeting,
                                   start_date=start_date,
                                   end_date=end_date,
                                   arrivals_slots=arrivals_slots)
