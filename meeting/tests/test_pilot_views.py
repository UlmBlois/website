from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz
from datetime import date, datetime

from django.contrib.messages import constants as messages
from django.conf import settings

from meeting.views.utils import PAGINATED_BY
from meeting.tests.utils import (create_meeting, create_time_slot,
                                 create_user, create_ulm, create_reservation,
                                 LoggedViewTestCase)
import logging
logger = logging.getLogger(__name__)


class PilotULMListTest(LoggedViewTestCase, TestCase):
    url = '/meeting/ulm/'
    url_name = 'pilot_ulm_list'
    template_name = 'pilot_ulm_list.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        for i in range(PAGINATED_BY+1):
            create_ulm(cls.user.pilot, 'F-JAZE')

    def test_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pilot_ulm_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['ulm_list']), PAGINATED_BY)

    def test_lists_all_ulms(self):
        # Get second page and confirm it has (exactly) remaining 1 item
        self.client.force_login(self.user)
        response = self.client.get(reverse('pilot_ulm_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['ulm_list']), 1)


class DeletePilotUlmTest(LoggedViewTestCase, TestCase):
    url = '/meeting/ulm/{}/delete/'
    url_name = 'pilot_delete_ulm'
    template_name = 'logged_delete_form.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ulm = create_ulm(cls.user.pilot, 'F-JAZE')

    def get_url(self):
        return self.url.format(self.ulm.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.ulm.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def test_constext_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cancel_url'],
                         reverse('pilot_ulm_list'))

    def test_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse('pilot_ulm_list'))

    def test_delete_messages_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, settings.MESSAGE_TAGS[messages.SUCCESS])

    def test_delete_messages_error(self):
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        ts = create_time_slot(meeting1,
                              tz.make_aware(
                                  datetime(2019, 8, 31, 10)),
                              3)
        create_reservation("1A", self.ulm, ts)
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, settings.MESSAGE_TAGS[messages.ERROR])


class PilotReservationListTest(LoggedViewTestCase, TestCase):
    url = '/meeting/reservation'
    url_name = 'pilot_reservation'
    template_name = 'pilot_reservation_list.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        ts = create_time_slot(meeting1,
                              tz.make_aware(
                                  datetime(2019, 8, 31, 10)),
                              3)

        ulm = create_ulm(cls.user.pilot, 'F-XAAA')
        for i in range(PAGINATED_BY+1):
            create_reservation(str(i), ulm, ts)

    def test_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pilot_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['reservation_list']), PAGINATED_BY)

    def test_lists_all_ulms(self):
        # Get second page and confirm it has (exactly) remaining 1 item
        self.client.force_login(self.user)
        response = self.client.get(reverse('pilot_reservation')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['reservation_list']), 1)
