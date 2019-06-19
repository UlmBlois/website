from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, datetime
from meeting.models import Meeting, TimeSlot, Pilot, Reservation, ULM
from meeting.tests.utils import create_meeting, create_time_slot


class MeetingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_meeting("1", date(2019, 8, 30), True)
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


class TimeSlotTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_meeting("1", date(2019, 8, 30), True)

    def test_clean(self):
        ts = TimeSlot()
        ts.meeting = Meeting.objects.get(name="1")
        ts.start_date = timezone.make_aware(
            datetime(2019, 8, 31, 10, 0))
        ts.end_date = timezone.make_aware(
            datetime(2019, 8, 31, 10, 30))
        ts.arrivals_slots = 5
        try:
            ts.clean()
        except ValidationError:
            self.fail("TimeSlot.clean raised ExceptionType unexpectedly!")
        ts.start_date = timezone.make_aware(
            datetime(2019, 8, 29, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = timezone.make_aware(
            datetime(2019, 9, 2, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = timezone.make_aware(
            datetime(2019, 8, 31, 10, 0))
        ts.end_date = timezone.make_aware(
            datetime(2019, 8, 29, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = timezone.make_aware(
            datetime(2019, 9, 2, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = timezone.make_aware(
            datetime(2019, 8, 31, 10, 30))
        ts.start_date = timezone.make_aware(
            datetime(2019, 8, 31, 11, 0))
        with self.assertRaises(ValidationError):
            ts.clean()

# TODO test create_or_update_user_profile


class PilotTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass


class ULMTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

# TODO test normalize_reservation


class ReservationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        ts1 = create_time_slot(meeting,
                               timezone.make_aware(datetime(2019, 8, 31, 10)),
                               5)
        ts2 = create_time_slot(meeting,
                               timezone.make_aware(datetime(2019, 8, 31, 11)),
                               5)
        user = User.objects.create_user(username='testuser', password='12345')
        Pilot.objects.filter(user=user).update(
            # insurance_company='AISCAIR',
            insurance_number='12345',
            licence_number='54321')
        ulm = ULM.objects.create(pilot=user.pilot,
                                 constructor='G1',
                                 model='Explorer',
                                 type='MU',
                                 imatriculation_country='FR',
                                 imatriculation='41-SOL',
                                 radio_id='F-JLOV')

        Reservation.objects.create(ulm=ulm,
                                   reservation_number='FAE1F6',
                                   time_slot=ts1,
                                   arrival=timezone.make_aware(
                                    datetime(2019, 8, 31, 11)),
                                   depart_time_slot=ts2,
                                   origin_city='Blois',
                                   origin_field='LFAZ',
                                   meeting=meeting)

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
        res.arrival = timezone.make_aware(datetime(2019, 8, 31, 15))
        self.assertFalse(res.is_on_time())

    def test_arrival_delay(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertEqual(res.arrival_delay().seconds/60, 30)
