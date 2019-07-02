from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from datetime import date, datetime
from unittest.mock import patch

from meeting.models import Meeting, TimeSlot, Reservation, Pilot, ULM
from meeting.tests.utils import (create_meeting, create_time_slot, create_ulm,
                                 create_user, create_reservation)


class MeetingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.meeting = create_meeting("1", date(2019, 8, 30), True)
        create_meeting("2", date(2018, 8, 30), False)

    def test_registration_open_at(self):  # same test as registration_open
        meeting = Meeting.objects.get(name="1")
        self.assertTrue(meeting.registration_open_at(
            date(2019, 7, 15)))
        self.assertFalse(meeting.registration_open_at(
            date(2019, 3, 1)))
        self.assertFalse(meeting.registration_open_at(
            date(2019, 5, 1)))

    def test_save(self):
        meeting2 = Meeting.objects.get(name="2")
        meeting2.active = True
        meeting2.save()
        self.assertTrue(Meeting.objects.get(name="2").active)
        self.assertFalse(Meeting.objects.get(name="1").active)
        Meeting.objects.filter(name="1").update(active=True)

    def test_open_days(self):
        days = [date(2019, 8, 30), date(2019, 8, 31), date(2019, 9, 1)]
        self.assertEqual(self.meeting.open_days(), days)


class TimeSlotTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_meeting("1", date(2019, 8, 30), True)

    def test_clean(self):
        ts = TimeSlot()
        ts.meeting = Meeting.objects.get(name="1")
        ts.start_date = tz.make_aware(
            datetime(2019, 8, 31, 10, 0))
        ts.end_date = tz.make_aware(
            datetime(2019, 8, 31, 10, 30))
        ts.arrivals_slots = 5
        try:
            ts.clean()
        except ValidationError:
            self.fail("TimeSlot.clean raised ExceptionType unexpectedly!")
        ts.start_date = tz.make_aware(
            datetime(2019, 8, 29, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = tz.make_aware(
            datetime(2019, 9, 2, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = tz.make_aware(
            datetime(2019, 8, 31, 10, 0))
        ts.end_date = tz.make_aware(
            datetime(2019, 8, 29, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = tz.make_aware(
            datetime(2019, 9, 2, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = tz.make_aware(
            datetime(2019, 8, 31, 10, 30))
        ts.start_date = tz.make_aware(
            datetime(2019, 8, 31, 11, 0))
        with self.assertRaises(ValidationError):
            ts.clean()

# TODO test create_or_update_user_profile


class PilotTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        ts = create_time_slot(meeting1,
                              tz.make_aware(
                                  datetime(2019, 8, 31, 10)),
                              3)
        cls.user = create_user('testuser', '12345')

        ulm = create_ulm(cls.user.pilot, 'F-XAAA')
        cls.res = create_reservation('FAE1F6', ulm, ts)

    def test_as_unconfirmed_reservation(self):
        self.assertTrue(self.user.pilot.as_unconfirmed_reservation)
        self.res.confirmed = True
        self.res.save()
        self.assertFalse(self.user.pilot.as_unconfirmed_reservation)

    def test_as_active_reservation(self):
        self.assertTrue(self.user.pilot.as_active_reservation)


class ULMTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('testuser', '12345')

    def test_normalize_ulm(self):
        create_ulm(self.user.pilot, 'f-jaer')
        self.assertEqual(ULM.objects.get(pilot=self.user.pilot).radio_id,
                         'F-JAER')

# TODO test normalize_reservation


class ReservationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        ts1 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 10)),
                               5)
        ts2 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 11)),
                               5)
        user = create_user('testuser', '12345')
        Pilot.objects.filter(user=user).update(
            # insurance_company='AISCAIR',
            insurance_number='12345',
            licence_number='54321')
        ulm = create_ulm(user.pilot, 'F-JLOV')
        create_reservation('FAE1F6', ulm, ts1, ts2,
                           tz.make_aware(datetime(2019, 8, 31, 11)))

#  TODO test validate_unique
    def test_is_active(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertTrue(res.is_active())
        Meeting.objects.filter(name="1").update(active=False)
        res = Reservation.objects.get(reservation_number='FAE1F6')

        self.assertFalse(res.is_active())
        Meeting.objects.filter(name="1").update(active=True)

    def test_is_missing_informations(self):  # TODO a completer
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertTrue(res.is_missing_informations())
        res.pilot.insurance_company = 'AISCAIR'
        self.assertFalse(res.is_missing_informations())

    def test_is_on_time(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertTrue(res.is_on_time())
        res.arrival = tz.make_aware(datetime(2019, 8, 31, 15))
        self.assertFalse(res.is_on_time())

    def test_arrival_delay(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertEqual(res.arrival_delay().seconds/60, 30)
