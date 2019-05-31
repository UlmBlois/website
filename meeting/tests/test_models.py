from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from meeting.models import Meeting, TimeSlot, Pilot, Reservation, ULM


class MeetingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(name="1",
                               registration_start=datetime.date(2019, 3, 15),
                               registration_end=datetime.date(2019, 4, 15),
                               start_date=datetime.date(2019, 8, 30),
                               end_date=datetime.date(2019, 9, 1),
                               active=True, fuel_aviable=100)
        Meeting.objects.create(name="2",
                               registration_start=datetime.date(2018, 3, 15),
                               registration_end=datetime.date(2018, 4, 15),
                               start_date=datetime.date(2018, 8, 30),
                               end_date=datetime.date(2018, 9, 1),
                               active=False, fuel_aviable=100)

    def test_registration_open_at(self):  # same test as registration_open
        meeting = Meeting.objects.get(name="1")
        self.assertTrue(meeting.registration_open_at(
            datetime.date(2019, 3, 15)))
        self.assertFalse(meeting.registration_open_at(
            datetime.date(2019, 3, 1)))
        self.assertFalse(meeting.registration_open_at(
            datetime.date(2019, 5, 1)))

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
        Meeting.objects.create(name="1",
                               registration_start=datetime.date(2019, 3, 15),
                               registration_end=datetime.date(2019, 4, 15),
                               start_date=datetime.date(2019, 8, 30),
                               end_date=datetime.date(2019, 9, 1),
                               active=True, fuel_aviable=100)

    def test_clean(self):
        ts = TimeSlot()
        ts.meeting = Meeting.objects.get(name="1")
        ts.start_date = timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10, 0))
        ts.end_date = timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10, 30))
        ts.arrivals_slots = 5
        try:
            ts.clean()
        except ValidationError:
            self.fail("TimeSlot.clean raised ExceptionType unexpectedly!")
        ts.start_date = timezone.make_aware(
            datetime.datetime(2019, 8, 29, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = timezone.make_aware(
            datetime.datetime(2019, 9, 2, 10, 0))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.start_date = timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10, 0))
        ts.end_date = timezone.make_aware(
            datetime.datetime(2019, 8, 29, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = timezone.make_aware(
            datetime.datetime(2019, 9, 2, 10, 30))
        with self.assertRaises(ValidationError):
            ts.clean()
        ts.end_date = timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10, 30))
        ts.start_date = timezone.make_aware(
            datetime.datetime(2019, 8, 31, 11, 0))
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
        Meeting.objects.create(name="1",
                               registration_start=datetime.date(2019, 3, 15),
                               registration_end=datetime.date(2019, 4, 15),
                               start_date=datetime.date(2019, 8, 30),
                               end_date=datetime.date(2019, 9, 1),
                               active=True, fuel_aviable=100)
        TimeSlot.objects.create(meeting=Meeting.objects.get(name="1"),
                                start_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 10)),
                                end_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 10, 30)),
                                arrivals_slots=5)
        User.objects.create_user(username='testuser', password='12345')
        user = User.objects.get(username='testuser')
        Pilot.objects.filter(user=user).update(
            # insurance_company='AISCAIR',
            insurance_number='12345',
            licence_number='54321')
        ULM.objects.create(pilot=Pilot.objects.get(user=user),
                           constructor='G1',
                           model='Explorer',
                           type='MU',
                           imatriculation_country='FR',
                           imatriculation='41-SOL',
                           radio_id='F-JLOV')
        ts = TimeSlot.objects.get(start_date=timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10)))
        Reservation.objects.create(ulm=ULM.objects.get(radio_id='F-JLOV'),
                                   reservation_number='FAE1F6',
                                   time_slot=ts,
                                   arrival=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 11)),
                                   depart_time_slot=ts,
                                   origin_city='Blois',
                                   origin_field='LF-41COQ')

#  TODO test validate_unique
    def test_clean(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        ts = TimeSlot.objects.get(start_date=timezone.make_aware(
            datetime.datetime(2019, 8, 31, 10)))
        res.time_slot = ts
        res.depart_time_slot = ts
        with self.assertRaises(ValidationError):
            res.clean()

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
        res.arrival = timezone.make_aware(datetime.datetime(2019, 8, 31, 15))
        self.assertFalse(res.is_on_time())

    def test_arrival_delay(self):
        res = Reservation.objects.get(reservation_number='FAE1F6')
        self.assertEqual(res.arrival_delay().seconds/60, 30)
