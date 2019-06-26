from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz
from datetime import date, datetime
from meeting.models import Pilot

from meeting.tests.utils import (create_meeting, create_time_slot, create_ulm,
                                 create_user, create_reservation,
                                 PermissionRequiredTestCase)

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

class StaffReservationValidationDetailTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/reservation/validation/{}/overview/'
    url_name = 'staff_reservation_overview'
    template_name = 'staff_reservation_validation.html'
    permission_required = ['reservation_validation']

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
        cls.reservation = create_reservation(
            'FAE1F6', ulm, ts1, ts2,
            tz.make_aware(datetime(2019, 8, 31, 11)))

    def get_url(self):
        return self.url.format(self.reservation.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.reservation.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['reservation'], self.reservation)


###############################################################################
# Reservation validation
###############################################################################


class StaffReservationValidationTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/reservation/validation/{}/validate/'
    url_name = 'staff_reservation_validate'
    permission_required = ['reservation_validation']
    redirect_url_name = 'staff_reservation_overview'

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
        cls.reservation = create_reservation(
            'FAE1F6', ulm, ts1, ts2,
            tz.make_aware(datetime(2019, 8, 31, 11)))

    def get_url(self):
        return self.url.format(self.reservation.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.reservation.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def get_redirect_url(self, args=None, kwargs=None):
        kwargs = {'pk': self.reservation.pk}
        return super().get_redirect_url(kwargs=kwargs)
