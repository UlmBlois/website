from django.test import TestCase
from datetime import date
from meeting.tests.utils import (create_meeting, ViewTestCase,
                                 LoggedViewTestCase)


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
