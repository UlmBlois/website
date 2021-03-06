from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date, datetime
from unittest.mock import patch

from meeting.models import Pilot, Reservation, ULM
from meeting.tests.utils import (create_meeting, create_time_slot, create_ulm,
                                 create_user, create_reservation,
                                 PermissionRequiredTestCase,
                                 create_full_reservation)

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
            'pilot_form-street_name': 'street',
            'pilot_form-mail_complement': 'comp',
            'pilot_form-city_code': 'city_code',
            'pilot_form-city': 'city',
            'pilot_form-country': 'FR',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())
        self.assertEqual(get_user_model().objects.get(pk=self.user.pk).first_name,
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


class StaffReservationUpdatePilotTest(StaffUpdatePilotTest):
    url = '/meeting/staff/reservation/validation/{0}/edit/pilot/{1}'
    url_name = 'staff_reservation_edit_pilot'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.res = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.res.pk, self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'res': self.res.pk,
                  'pk': self.user.pilot.pk
                 }
        return reverse(self.url_name, kwargs=kwargs)

    def get_success_url(self):
        return reverse('staff_reservation_overview',
                       kwargs={'pk': self.res.pk})


###############################################################################
# ULM related View
###############################################################################

class StaffUpdatePilotULMTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/pilot/{0}/edit/ulm/{1}/'
    url_name = 'staff_update_ulm'
    template_name = 'base_logged_form.html'
    permission_required = ['reservation_validation']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ulm = create_ulm(cls.user.pilot, 'F-JAZE')

    def get_url(self):
        return self.url.format(self.user.pilot.pk, self.ulm.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'pilot': self.user.pilot.pk,
                  'pk': self.ulm.pk
                  }
        return super().get_url_from_name(kwargs=kwargs)

    def get_success_url(self):
        return reverse('pilot_overview', kwargs={'pk': self.user.pilot.pk})

    def test_form_valid(self):
        form_data = {
            'constructor': 'Dasault',
            'model': 'Mirage III',
            'type': 'MU',
            'imatriculation_country': 'FR',
            'imatriculation': 'Azerty',
            'radio_id_0': 'F-',
            'radio_id_1': 'JAZA'
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())
        self.assertEqual(ULM.objects.get(radio_id='F-JAZA').constructor,
                         form_data['constructor'])

    def test_form_invalid(self):
        form_data = {
            'constructor': 'Dasault',
            'model': 'Mirage III',
            'type': 'MU',
            'imatriculation_country': 'FR',
            'imatriculation': 'Azerty',
            'radio_id_0': 'F-',
            'radio_id_1': 'JAZ'  # invalid registration number
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ULM.objects.filter(radio_id='F-JAZ').exists())
        self.assertTrue(ULM.objects.filter(radio_id='F-JAZE').exists())


class StaffReservationUpdatePilotULMTest(StaffUpdatePilotULMTest):
    url = '/meeting/staff/reservation/validation/{0}/edit/ulm/{1}'
    url_name = 'staff_reservation_edit_ulm'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.res = create_full_reservation(ulm=cls.ulm)

    def get_url(self):
        return self.url.format(self.res.pk, self.ulm.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'res': self.res.pk,
                  'pk': self.ulm.pk
                  }
        return reverse(self.url_name, kwargs=kwargs)

    def get_success_url(self):
        return reverse('staff_reservation_overview',
                       kwargs={'pk': self.res.pk})

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
        cls.reservation = create_full_reservation()

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


class StaffReservationUpdateTest(PermissionRequiredTestCase, TestCase):
    url = '/meeting/staff/reservation/validate/edit/{0}'
    url_name = 'staff_reservation_edit'
    template_name = 'base_logged_form.html'
    permission_required = ['reservation_validation']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reservation = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.reservation.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.reservation.pk}
        return reverse(self.url_name, kwargs=kwargs)

    def get_success_url(self):
        return reverse('staff_reservation_overview',
                       kwargs={'pk': self.reservation.pk})

    def test_form_valid(self):
        form_data = {
            'ulm': self.reservation.ulm.pk,
            'time_slot': self.reservation.time_slot.pk,
            'depart_time_slot': self.reservation.depart_time_slot.pk,
            'fuel_reservation': 10,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())  # todo change
        self.assertEqual(
            Reservation.objects.get(pk=self.reservation.pk).fuel_reservation,
            form_data['fuel_reservation'])

    def test_form_invalid(self):
        form_data = {
            'ulm': self.reservation.ulm.pk,
            'time_slot': self.reservation.time_slot.pk,
            'depart_time_slot': self.reservation.depart_time_slot.pk,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Reservation.objects.get(pk=self.reservation.pk).fuel_reservation,
            0)


class StaffUpdatePilotReservationTest(StaffReservationUpdateTest):
    url = '/meeting/staff/pilot/{}/edit/reservation/{}'
    url_name = 'staff_update_reservation'

    def get_url(self):
        return self.url.format(self.user.pilot.pk, self.reservation.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pilot': self.reservation.pilot.pk,
                  'pk': self.reservation.pk,
                  }
        return reverse(self.url_name, kwargs=kwargs)

    def get_success_url(self):
        return reverse('pilot_overview',
                       kwargs={'pk': self.user.pilot.pk})

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
            'FAE1F6', ulm, ts1, ts2)

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
