from django.test import TestCase
from django.utils import timezone as tz

from datetime import date, datetime

from meeting.tests import utils
from meeting import admin
from meeting import models


class ArrivalFilterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = utils.create_meeting('1', date(2019, 8, 30))
        cls.res1 = utils.create_full_reservation(
                        res_num='11111',
                        meeting=meeting,
                        arrival=tz.make_aware(datetime(2019, 8, 30, 10)))
        user = utils.create_user('testuser2', '12345')
        cls.res2 = utils.create_full_reservation(
                        res_num='22222',
                        meeting=meeting,
                        user=user)

    def test_filter_arrived(self):
        filter = admin.ArrivalFilter(
                        None,
                        {'is_arrived': 'yes'},
                        models.Reservation,
                        admin.ReservationAdmin).queryset(
                            None,
                            models.Reservation.objects.all())
        self.assertEqual(len(filter), 1)
        self.assertQuerysetEqual(filter, [repr(self.res1)])

    def test_filter_not_arrived(self):
        filter = admin.ArrivalFilter(
                        None,
                        {'is_arrived': 'no'},
                        models.Reservation,
                        admin.ReservationAdmin).queryset(
                            None,
                            models.Reservation.objects.all())
        self.assertEqual(len(filter), 1)
        self.assertQuerysetEqual(filter, [repr(self.res2)])

    def test_filter_all(self):
        filter = admin.ArrivalFilter(
                        None,
                        {},
                        models.Reservation,
                        admin.ReservationAdmin).queryset(
                            None,
                            models.Reservation.objects.all())
        self.assertEqual(len(filter), 2)
        self.assertQuerysetEqual(filter,
                                 [repr(self.res1), repr(self.res2)],
                                 ordered=False)
