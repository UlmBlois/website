from django.test import TestCase
from django.utils import timezone as tz
from datetime import date, datetime

from meeting.filters import ReservationFilter
from meeting.models import Reservation
from meeting.tests.utils import (create_meeting, create_time_slot, create_ulm,
                                 create_user, create_reservation,)


class ReservationFilterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        meeting = create_meeting("1", date(2019, 8, 30), True)
        ts1 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 10)),
                               5)
        ts2 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 11)),
                               5)
        user = create_user('testuser', '12345')
        ulm = create_ulm(user.pilot, 'F-JLOV')
        cls.res1 = create_reservation(
            'FAE1F6', ulm, ts1, ts2, fuel_reservation=10)
        user = create_user('testuser2', '12345')
        ulm = create_ulm(user.pilot, 'F-JLAV')
        cls.res2 = create_reservation(
            'FAE1F7', ulm, ts1, ts2)

    def test_filter_numeric_is_set(self):
        filterset = ReservationFilter()
        result = filterset.filter_numeric_is_set(Reservation.objects.all(),
                                                 'fuel_reservation',
                                                 False)
        expected = [self.res2]
        self.assertQuerysetEqual(result, [repr(x) for x in expected])

        result = filterset.filter_numeric_is_set(Reservation.objects.all(),
                                                 'fuel_reservation',
                                                 True)
        expected = [self.res1]
        self.assertQuerysetEqual(result, [repr(x) for x in expected])
