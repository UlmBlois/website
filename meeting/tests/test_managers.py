from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from meeting.models import Meeting, TimeSlot, Reservation, ULM

from meeting.tests.utils import create_meeting, create_time_slot


class MeetingManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        create_meeting("1", datetime.date(2019, 8, 30), True)
        create_meeting("2", datetime.date(2018, 8, 30), False)

    def test_active(self):
        meeting = Meeting.objects.active()
        self.assertTrue(meeting.active)
        self.assertEqual(meeting.name, "1")


class TimeSlotManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        meeting1 = create_meeting("1", datetime.date(2019, 8, 30), True)
        meeting2 = create_meeting("2", datetime.date(2018, 8, 30), False)
        ts = create_time_slot(meeting1,
                              timezone.make_aware(
                                  datetime.datetime(2019, 8, 31, 10)),
                              3)
        create_time_slot(meeting1,
                         timezone.make_aware(
                            datetime.datetime(2019, 8, 31, 11)),
                         0)
        create_time_slot(meeting2,
                         timezone.make_aware(
                            datetime.datetime(2018, 8, 31, 11)),
                         5)

        user = User.objects.create_user(username='testuser', password='12345')

        ulm = ULM.objects.create(radio_id='F-XAAA', pilot=user.pilot)
        Reservation.objects.create(reservation_number='FAE1F6',
                                   time_slot=ts,
                                   meeting=ts.meeting,
                                   ulm=ulm)
        Reservation.objects.create(reservation_number='FAD1F7',
                                   time_slot=ts,
                                   meeting=ts.meeting,
                                   ulm=ulm)

    def test_actives(self):
        ts = TimeSlot.objects.actives()
        self.assertEqual(ts.count(), 2)

    def test_aviables(self):
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 1)
        Reservation.objects.create(reservation_number='FAE1F8',
                                   time_slot=ts.first(),
                                   meeting=ts.first().meeting,
                                   ulm=ULM.objects.get(radio_id='F-XAAA'))
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 0)
