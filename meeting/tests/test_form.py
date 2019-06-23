from django.test import TestCase
from django.utils import timezone as tz
from datetime import date, datetime

from meeting.form import ReservationForm
from meeting.tests.utils import (create_meeting, create_time_slot,
                                 create_user, create_ulm)


class ReservationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        cls.ts1 = create_time_slot(meeting,
                                   tz.make_aware(
                                    datetime(2019, 8, 31, 10)),
                                   3)
        cls.ts2 = create_time_slot(meeting,
                                   tz.make_aware(
                                    datetime(2019, 8, 31, 11)),
                                   3)
        cls.ts3 = create_time_slot(meeting,
                                   tz.make_aware(
                                    datetime(2019, 8, 31, 12)),
                                   0)
        cls.user = create_user("user", "testtest")
        user2 = create_user("user2", "testtest")
        cls.ulm = create_ulm(cls.user.pilot, 'F-JAZE')
        create_ulm(user2.pilot, 'F-JAZR')

    def test_initialisation(self):
        form = ReservationForm(pilot=self.user.pilot)
        self.assertEqual(form.fields['ulm'].queryset.count(), 1)
        ts_queryset = form.fields['time_slot'].queryset
        self.assertEqual(ts_queryset.count(), 2)
        self.assertFalse(ts_queryset.filter(pk=self.ts3.pk).exists())
        self.assertQuerysetEqual(form.fields['depart_time_slot'].queryset,
                                 ts_queryset, ordered=False,
                                 transform=lambda x: x)

    def test_clean(self):
        form = ReservationForm(pilot=self.user.pilot)
        self.assertFalse(form.is_valid())
        form_data = {
            'ulm': self.ulm.id,
            'time_slot': self.ts1.id,
            'depart_time_slot': self.ts2.id,
            'fuel_reservation': 0
        }
        form = ReservationForm(pilot=self.user.pilot, data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_timeslots_equals(self):
        form_data = {
            'ulm': self.ulm.id,
            'time_slot': self.ts1.id,
            'depart_time_slot': self.ts1.id,
            'fuel_reservation': 0
        }
        form = ReservationForm(pilot=self.user.pilot, data=form_data)
        self.assertFalse(form.is_valid())

    def test_clean_departure_anterior_arrival(self):
        form_data = {
            'ulm': self.ulm.id,
            'time_slot': self.ts2.id,
            'depart_time_slot': self.ts1.id,
            'fuel_reservation': 0
        }
        form = ReservationForm(pilot=self.user.pilot, data=form_data)
        self.assertFalse(form.is_valid())
