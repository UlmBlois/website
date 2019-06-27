from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz
from django.contrib.auth.models import User

from datetime import date, datetime
from unittest.mock import patch

from meeting.models import Pilot, Reservation
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


class StaffUpdatePilotTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/pilot/{}/edit/profile/'
    url_name = 'staff_update_pilot'
    template_name = 'base_logged_form.html'
    permission_required = ['reservation_validation']

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def get_success_url(self):
        return reverse('pilot_overview', kwargs={'pk': self.user.pilot.pk})

    def test_form_valid(self):
        form_data = {
            'user_form-username': 'test',
            'user_form-first_name': 'test',
            'user_form-last_name': 'test',
            'user_form-email': 'test@test.fr',
            'pilot_form-insurance_company': 'Air COURTAGE',
            'pilot_form-insurance_number': 'aaaaaaa',
            'pilot_form-licence_number': 'azer',
            'pilot_form-phone_number_0': '+33',
            'pilot_form-phone_number_1': '645454545',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())
        self.assertEqual(User.objects.get(pk=self.user.pk).first_name,
                         form_data['user_form-first_name'])
        self.assertEqual(
            Pilot.objects.get(pk=self.user.pilot.pk).insurance_number,
            form_data['pilot_form-insurance_number'])

    def test_form_invalid(self):
        form_data = {
            'user_form-username': 'test',
            'user_form-first_name': 'test',
            'user_form-last_name': 'test',
            'user_form-email': 'test@test.fr',
            'pilot_form-insurance_company': 'Air COURTAGE',
            'pilot_form-insurance_number': 'aaaaaaa',
            'pilot_form-licence_number': 'azer',
            'pilot_form-phone_number_0': '+33',
            'pilot_form-phone_number_1': '0',   # invalid phone number
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Pilot.objects.get(pk=self.user.pilot.pk).licence_number, '')

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

    def test_get(self):
        with patch.object(tz,
                          'now', return_value=tz.make_aware(
                                        datetime(2019, 8, 31, 10, 15))
                          ) as mock_now:
            self.client.force_login(self.user)
            self.reservation.arrival = None
            self.reservation.save()
            self.assertIsNone(self.reservation.arrival)
            response = self.client.get(self.get_url())
            self.assertRedirects(response, self.get_redirect_url())
            self.assertEqual(
                Reservation.objects.get(reservation_number='FAE1F6').arrival,
                mock_now())

    def test_reservation_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)


class StaffReservationInvalidation(StaffReservationValidationTest):
    url = '/meeting/staff/reservation/validation/{}/invalidate/'
    url_name = 'staff_reservation_invalidate'

    def test_get(self):
        self.client.force_login(self.user)
        self.reservation.arrival = tz.make_aware(
                      datetime(2019, 8, 31, 10, 15))
        self.reservation.save()
        response = self.client.get(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        self.assertIsNone(
            Reservation.objects.get(reservation_number='FAE1F6').arrival)
