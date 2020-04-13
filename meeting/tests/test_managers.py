from django.test import TestCase
from django.utils import timezone as tz
from datetime import datetime, date
from meeting.models import Meeting, TimeSlot, ULM, Reservation

from meeting.tests.utils import (create_meeting, create_time_slot, create_ulm,
                                 create_user, create_reservation,
                                 create_full_reservation)


class MeetingManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_meeting("1", date(2019, 8, 30), True)
        create_meeting("2", date(2018, 8, 30), False)

    def test_active(self):
        meeting = Meeting.objects.active()
        self.assertTrue(meeting.active)
        self.assertEqual(meeting.name, "1")


class TimeSlotManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        meeting2 = create_meeting("2", date(2018, 8, 30), False)
        cls.ts = create_time_slot(meeting1,
                                  tz.make_aware(
                                    datetime(2019, 8, 31, 10)),
                                  3)

        cls.ts3 = create_time_slot(meeting1,
                                   tz.make_aware(
                                    datetime(2019, 8, 31, 11)),
                                   2)
        cls.ts2 = create_time_slot(meeting2,
                                   tz.make_aware(
                                    datetime(2018, 8, 31, 11)),
                                   3)
        user = create_user('testuser', '12345')
        ulm = create_ulm(user.pilot, 'F-XAAA')
        create_reservation('FAE1F6', ulm, cls.ts, cls.ts2)
        create_reservation('FAD1F7', ulm, cls.ts, cls.ts2)

    def test_actives(self):
        ts = TimeSlot.objects.actives()
        self.assertEqual(ts.count(), 2)

    def test_departures_slots_left(self):
        departure = TimeSlot.objects.departures_slots_left()
        self.assertEqual(departure.count(), 2)
        create_reservation('FAE1F8',
                           ULM.objects.get(radio_id='F-XAAA'),
                           self.ts, self.ts2)
        create_reservation('FAE1F9',
                           ULM.objects.get(radio_id='F-XAAA'),
                           self.ts2, self.ts3)
        create_reservation('FAE1FA',
                           ULM.objects.get(radio_id='F-XAAA'),
                           self.ts2, self.ts3)
        departure = TimeSlot.objects.departures_slots_left()
        self.assertEqual(departure.count(), 1)

    def test_arrivals_slots_left(self):
        ts = TimeSlot.objects.arrivals_slots_left()
        self.assertEqual(ts.count(), 2)
        create_reservation('FAE1F8',
                           ULM.objects.get(radio_id='F-XAAA'),
                           ts.first())
        ts = TimeSlot.objects.arrivals_slots_left()
        self.assertEqual(ts.count(), 1)


class ReservationManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        meeting2 = create_meeting("2", date(2018, 8, 30), False)

        user1 = create_user('user1', '12345')
        user2 = create_user('user2', '12345')
        user3 = create_user('user3', '12345')
        create_full_reservation(res_num='FAAAAA', meeting=meeting2)
        res1 = create_full_reservation(res_num='FAE1F6', user=user1,
                                       meeting=meeting)
        res2 = create_full_reservation(res_num='FAE1F7', user=user2,
                                       meeting=meeting, canceled=True)
        res3 = create_full_reservation(res_num='FAE1F8', user=user3,
                                       meeting=meeting, confirmed=True)
        cls.actives = [res1, res2, res3]
        cls.unconfirmed_actives = [res1]

    def test_actives(self):
        actives = Reservation.objects.actives()
        self.assertQuerysetEqual(actives, [repr(x) for x in self.actives],
                                 ordered=False)

    def test_unconfirmed_active(self):
        unconfirmed_actives = Reservation.objects.unconfirmed_actives()
        self.assertQuerysetEqual(unconfirmed_actives,
                                 [repr(x) for x in self.unconfirmed_actives],
                                 ordered=False)
