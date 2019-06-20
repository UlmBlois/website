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


def create_ulm(pilot, radio_id):
    return ULM.objects.create(pilot=pilot,
                              radio_id=radio_id,
                              )


def create_user(name, password):
    return User.objects.create_user(username=name, password=password)


def create_reservation(res_num, ulm, ts1, ts2=None, arrival=None):
    return Reservation.objects.create(
                ulm=ulm,
                pilot=ulm.pilot,
                reservation_number=res_num,
                time_slot=ts1,
                arrival=arrival,
                depart_time_slot=ts2,
                meeting=ts1.meeting)
