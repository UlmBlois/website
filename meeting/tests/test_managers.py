from django.test import TestCase
from django.utils import timezone as tz
from datetime import datetime, date
from meeting.models import Meeting, TimeSlot, ULM

from meeting.tests.utils import create_meeting, create_time_slot, create_ulm, create_user, create_reservation


class MeetingManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        create_meeting("1", date(2019, 8, 30), True)
        create_meeting("2", date(2018, 8, 30), False)

    def test_active(self):
        meeting = Meeting.objects.active()
        self.assertTrue(meeting.active)
        self.assertEqual(meeting.name, "1")


class TimeSlotManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        meeting2 = create_meeting("2", date(2018, 8, 30), False)
        ts = create_time_slot(meeting1,
                              tz.make_aware(
                                  datetime(2019, 8, 31, 10)),
                              3)
        create_time_slot(meeting1,
                         tz.make_aware(
                            datetime(2019, 8, 31, 11)),
                         0)
        create_time_slot(meeting2,
                         tz.make_aware(
                            datetime(2018, 8, 31, 11)),
                         5)

        user = create_user('testuser', '12345')

        ulm = create_ulm(user.pilot, 'F-XAAA')
        create_reservation('FAE1F6', ulm, ts)
        create_reservation('FAD1F7', ulm, ts)

    def test_actives(self):
        ts = TimeSlot.objects.actives()
        self.assertEqual(ts.count(), 2)

    def test_aviables(self):
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 1)
        create_reservation('FAE1F8',
                           ULM.objects.get(radio_id='F-XAAA'),
                           ts.first())
        ts = TimeSlot.objects.aviables()
        self.assertEqual(ts.count(), 0)
