from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz
from datetime import date, datetime

from django.contrib.messages import constants as messages
from django.conf import settings
from django.contrib.auth import get_user_model


from freezegun import freeze_time

from meeting.views.utils import PAGINATED_BY
from meeting.tests.utils import (create_meeting, create_time_slot,
                                 create_ulm, create_reservation,
                                 LoggedViewTestCase)
from meeting.models import ULM, Reservation, Pilot

import logging
logger = logging.getLogger(__name__)


###############################################################################
# Pilot related View
###############################################################################
class DetailPilotTest(LoggedViewTestCase, TestCase):
    url = '/meeting/pilot/{}/detail/'
    url_name = 'pilot'
    template_name = 'pilot_profile.html'

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)


class UpdateUserPilotViewTest(LoggedViewTestCase, TestCase):
    url = '/meeting/pilot/{}/edit/'
    url_name = 'edit_pilot'
    template_name = 'base_logged_form.html'

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.user.pilot.pk})

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pilot'], self.user.pilot)

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
            'pilot_form-phone_number_1': '0',  # invalid phone number
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Pilot.objects.get(pk=self.user.pilot.pk).licence_number, '')


class PilotChangePasswordTest(LoggedViewTestCase, TestCase):
    url = '/meeting/pilot/password/'
    url_name = 'change_password'
    template_name = 'base_logged_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.user.pilot.pk})

    def test_form_valid(self):
        form_data = {
            'old_password': 'testtest',
            'new_password1': 'testtest2',
            'new_password2': 'testtest2',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())
        usr = get_user_model().objects.get(pk=self.user.pk)
        self.assertTrue(usr.check_password(form_data['new_password1']))

    def test_form_invalid(self):
        form_data = {
            'old_password': 'testtest',
            'new_password1': 'testtest1',
            'new_password2': 'testtest2',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        usr = get_user_model().objects.get(pk=self.user.pk)
        self.assertFalse(usr.check_password(form_data['new_password1']))

###############################################################################
# ULM related View
###############################################################################


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

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cancel_url'],
                         reverse('pilot_ulm_list'))

    def test_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse('pilot_ulm_list'))

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ULM.objects.filter(pk=self.ulm.pk).exists())

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


class CreatePilotULMTest(LoggedViewTestCase, TestCase):
    url = '/meeting/ulm/new/'
    url_name = 'pilot_create_ulm'
    template_name = 'base_logged_form.html'

    def test_form_valid(self):
        form_data = {
            'constructor': 'Dasault',
            'model': 'Mirage III',
            'type': 'MU',
            'imatriculation_country': 'FR',
            'imatriculation': 'Azerty',
            'radio_id_0': 'F-',
            'radio_id_1': 'JAZE'
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, reverse('pilot_ulm_list'))
        self.assertEqual(self.user.pilot,
                         ULM.objects.get(radio_id='F-JAZE').pilot)


class UpdatePilotULM(LoggedViewTestCase, TestCase):
    url = '/meeting/ulm/{}/edit/'
    url_name = 'pilot_update_ulm'
    template_name = 'base_logged_form.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ulm = create_ulm(cls.user.pilot, 'F-JAZE')

    def get_url(self):
        return self.url.format(self.ulm.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.ulm.pk}
        return super().get_url_from_name(kwargs=kwargs)

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
        self.assertRedirects(response, reverse('pilot_ulm_list'))
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

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ulm'], self.ulm)

###############################################################################
# Reservation related View
###############################################################################


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
        self.assertEqual(len(response.context['reservation_list']),
                         PAGINATED_BY)

    def test_lists_all_ulms(self):
        # Get second page and confirm it has (exactly) remaining 1 item
        self.client.force_login(self.user)
        response = self.client.get(reverse('pilot_reservation')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['reservation_list']), 1)


@freeze_time("2019-08-10")
class CreatePilotReservationTest(LoggedViewTestCase, TestCase):
    url = '/meeting/reservation/new'
    url_name = 'pilot_create_reservation'
    template_name = 'base_logged_form.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        cls.ts1 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 10)),
                                   3)
        cls.ts2 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 11)),
                                   3)
        cls.ulm = create_ulm(cls.user.pilot, 'F-XAAA')

    def test_form_valid(self):
        form_data = {
            'ulm': self.ulm.pk,
            'time_slot': self.ts1.pk,
            'depart_time_slot': self.ts2.pk,
            'fuel_reservation': 0,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, reverse('pilot_reservation'))
        self.assertTrue(Reservation.objects.filter(ulm=self.ulm.pk).exists())

    def test_form_invalid(self):
        form_data = {
            'ulm': self.ulm.pk,
            'time_slot': self.ts1.pk,
            'depart_time_slot': self.ts2.pk,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(ulm=self.ulm.pk).exists())

    def test_registration_open(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    @freeze_time("2019-08-30")
    def test_registration_close(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 403)


class UpdatePilotReservationTest(LoggedViewTestCase, TestCase):
    url = '/meeting/reservation/{}/edit'
    url_name = 'pilot_update_reservation'
    template_name = 'base_logged_form.html'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        cls.ts1 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 10)),
                                   3)
        cls.ts2 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 11)),
                                   3)

        cls.ulm = create_ulm(cls.user.pilot, 'F-XAAA')
        cls.res = create_reservation("abcd", cls.ulm, cls.ts1, cls.ts2)

    def get_url(self):
        return self.url.format(self.res.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.res.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def test_form_valid(self):
        form_data = {
            'ulm': self.ulm.pk,
            'time_slot': self.ts1.pk,
            'depart_time_slot': self.ts2.pk,
            'fuel_reservation': 10,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, reverse('pilot_reservation'))
        self.assertEqual(
            Reservation.objects.get(pk=self.res.pk).fuel_reservation, 10)

    def test_form_invalid(self):
        form_data = {
            'ulm': self.ulm.pk,
            'time_slot': self.ts1.pk,
            'depart_time_slot': self.ts2.pk,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Reservation.objects.get(pk=self.res.pk).fuel_reservation, 0)


###############################################################################
# Reservation related View
###############################################################################

class ReservationWizardStep1Test(UpdateUserPilotViewTest):
    url = '/meeting/reservation/wizard/{}/user'
    url_name = 'reservation_wizard_step1'

    def get_success_url(self):
        return reverse('reservation_wizard_step2',
                       kwargs={'pilot': self.user.pilot.pk})


class ReservationWizardStep2Test(LoggedViewTestCase, TestCase):
    url = '/meeting/reservation/wizard/{}/ulm'
    url_name = 'reservation_wizard_step2'
    template_name = 'base_logged_form.html'
    # NICETODO see if more test are needed

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        meeting1 = create_meeting("1", date(2019, 8, 30), True)
        cls.ts1 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 10)),
                                   3)
        cls.ts2 = create_time_slot(meeting1,
                                   tz.make_aware(
                                        datetime(2019, 8, 31, 11)),
                                   3)
        cls.ulm = create_ulm(cls.user.pilot, 'F-JAZE')

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pilot': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)

    @freeze_time("2019-08-10")
    def test_formset_valid(self):
        formset_data = {
            # management_form data
            'form-INITIAL_FORMS': '1',
            'form-TOTAL_FORMS': '1',

            # form 0
            'form-0-constructor': 'Dasault',
            'form-0-model': 'Mirage III',
            'form-0-type': 'MU',
            'form-0-imatriculation_country': 'FR',
            'form-0-imatriculation': 'Azerty',
            'form-0-radio_id_0': 'F-',
            'form-0-radio_id_1': 'JAZA',
            'form-0-id': str(self.ulm.pk),
        }
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), formset_data)
        self.assertRedirects(response, reverse('pilot_create_reservation'))
        self.assertEqual(
            ULM.objects.filter(pilot=self.user.pilot.pk).count(), 1)
        formset_data['form-TOTAL_FORMS'] = '2'
        formset_data.update({
            'form-1-constructor': '1',
            'form-1-model': '1',
            'form-1-type': 'MU',
            'form-1-imatriculation_country': 'FR',
            'form-1-imatriculation': '1',
            'form-1-radio_id_0': 'F-',
            'form-1-radio_id_1': 'JAER',
            'form-1-id': '',
        })
        response = self.client.post(self.get_url(), formset_data)
        self.assertRedirects(response, reverse('pilot_create_reservation'))
        self.assertEqual(
            ULM.objects.filter(pilot=self.user.pilot.pk).count(), 2)
