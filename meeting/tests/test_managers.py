from django.test import TestCase
from django.utils import timezone
import datetime
from meeting.models import Meeting, TimeSlot, Reservation


class MeetingManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
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

    def test_active(self):
        meeting = Meeting.objects.active()
        self.assertTrue(meeting.active)


class TimeSlotManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
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
        TimeSlot.objects.create(meeting=Meeting.objects.get(name="1"),
                                start_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 10)),
                                end_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 10, 30)),
                                arrivals_slots=3)
        TimeSlot.objects.create(meeting=Meeting.objects.get(name="1"),
                                start_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 11)),
                                end_date=timezone.make_aware(
                                    datetime.datetime(2019, 8, 31, 11, 30)),
                                arrivals_slots=0)
        TimeSlot.objects.create(meeting=Meeting.objects.get(name="2"),
                                start_date=timezone.make_aware(
                                    datetime.datetime(2018, 8, 31, 11)),
                                end_date=timezone.make_aware(
                                    datetime.datetime(2018, 8, 31, 11, 30)),
                                arrivals_slots=5)
        ts = TimeSlot.objects.get(start_date=timezone.make_aware(
                datetime.datetime(2019, 8, 31, 10)))
        Reservation.objects.create(reservation_number='FAE1F6',
                                   time_slot=ts)
        Reservation.objects.create(reservation_number='FAD1F7',
                                   time_slot=ts)

    def test_actives(self):
        ts = TimeSlot.objects.actives()
        self.assertEqual(ts.count(), 2)

    def test_aviables(self):
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 1)
        Reservation.objects.filter(reservation_number='FAD1F7').update(
            depart_time_slot=ts.first())
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 0)
