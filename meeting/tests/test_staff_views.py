from django.test import TestCase
from django.urls import reverse

from meeting.tests.utils import PermissionRequiredTestCase

###############################################################################
# Pilot related View
###############################################################################


class PilotOverviewTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/pilot/{}/overview/'
    url_name = 'pilot_overview'
    template_name = 'pilot_summary.html'
    permission_required = ['reservation_validation']

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pilot'], self.user.pilot)


###############################################################################
# Reservation related View
###############################################################################
