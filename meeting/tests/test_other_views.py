from django.test import TestCase
from django.utils import timezone as tz

from datetime import date, datetime

from meeting.tests.utils import (create_meeting, create_time_slot,
                                 ViewTestCase, LoggedViewTestCase)


class IndexViewTest(ViewTestCase, TestCase):
    url = '/meeting/'
    url_name = 'index'
    template_name = 'index.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.meeting = create_meeting("1", date(2019, 8, 30), True)

    def test_context_data(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['meeting'], self.meeting)


class LoggedIndexViewTest(LoggedViewTestCase, TestCase):
    url = '/meeting/pilot/'
    url_name = 'logged_index'
    template_name = 'logged_index.html'


class TimeSlotAviableViewTest(ViewTestCase, TestCase):
    url = '/meeting/slot/aviable'
    url_name = 'slot_aviable'
    template_name = 'aviable_timeslot.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.meeting = create_meeting("1", date(2019, 8, 30), True)
        cls.ts1 = create_time_slot(cls.meeting,
                                   tz.make_aware(datetime(2019, 8, 31, 10)),
                                   5)
        cls.ts2 = create_time_slot(cls.meeting,
                                   tz.make_aware(datetime(2019, 8, 30, 11)),
                                   0)
        cls.ts3 = create_time_slot(cls.meeting,
                                   tz.make_aware(datetime(2019, 8, 30, 9)),
                                   0)

    def test_context_data(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['meeting'], self.meeting)
        self.assertEqual(list(response.context['ts_aviables']), [self.ts1])
        ts_t = [[date(2019, 8, 30), date(2019, 8, 31), date(2019, 9, 1)],
                (self.ts3, self.ts1, None), (self.ts2, None, None)]
        self.assertEqual(response.context['ts_table'], ts_t)
