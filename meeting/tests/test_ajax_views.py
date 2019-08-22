from django.test import TestCase
from django.contrib.auth.models import Permission

from meeting.models import Reservation
from meeting.tests.utils import (create_full_reservation,
                                 LoggedViewTestCase,
                                 PermissionRequiredTestCase)


class test_ajax_cancel_reservation(LoggedViewTestCase, TestCase):
    url = '/meeting/ajax/reservation/cancel/{0}'
    url_name = 'ajax_cancel_reservation'
    redirect_url_name = 'pilot_reservation'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.res = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.res.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'pk': self.res.pk,
                 }
        return super().get_url_from_name(kwargs=kwargs)

    def test_reservation_canceled(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertTrue(res.canceled)


class test_ajax_confirm_reservation(LoggedViewTestCase, TestCase):
    url = '/meeting/ajax/reservation/confirm/{0}'
    url_name = 'ajax_confirm_reservation'
    redirect_url_name = 'pilot_reservation'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.res = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.res.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'pk': self.res.pk,
                 }
        return super().get_url_from_name(kwargs=kwargs)

    def test_reservation_confirmed(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertTrue(res.is_confirmed)

    def test_try_confirme_canceled_reservation(self):
        self.client.force_login(self.user)
        self.res.cancel()
        self.res.save()
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertFalse(res.is_confirmed())


# TODO upgrade to PermissionRequiredTestCase
class test_ajax_staff_cancel_reservation(LoggedViewTestCase, TestCase):
    url = '/meeting/ajax/staff/reservation/cancel/{0}'
    url_name = 'ajax_staff_cancel_reservation'
    redirect_url_name = 'staff_reservation_overview'
    permission_required = ['reservation_validation']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        permissions = Permission.objects.get(
            codename__in=cls.permission_required)
        cls.user.user_permissions.add(permissions)
        cls.user.save()
        cls.res = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.res.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'pk': self.res.pk,
                 }
        return super().get_url_from_name(kwargs=kwargs)

    def get_redirect_url(self):
        return super().get_redirect_url(kwargs={'pk': self.res.pk})

    def test_reservation_canceled(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertTrue(res.canceled)


# TODO upgrade to PermissionRequiredTestCase
class test_ajax_staff_confirm_reservation(LoggedViewTestCase, TestCase):
    url = '/meeting/ajax/staff/reservation/confirm/{0}'
    url_name = 'ajax_staff_confirm_reservation'
    redirect_url_name = 'staff_reservation_overview'
    permission_required = ['reservation_validation']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        permissions = Permission.objects.get(
            codename__in=cls.permission_required)
        cls.user.user_permissions.add(permissions)
        cls.user.save()
        cls.res = create_full_reservation(user=cls.user)

    def get_url(self):
        return self.url.format(self.res.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {
                  'pk': self.res.pk,
                 }
        return super().get_url_from_name(kwargs=kwargs)

    def get_redirect_url(self):
        return super().get_redirect_url(kwargs={'pk': self.res.pk})

    def test_reservation_confirmed(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertTrue(res.is_confirmed)

    def test_try_confirme_canceled_reservation(self):
        self.client.force_login(self.user)
        self.res.cancel()
        self.res.save()
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.get_redirect_url())
        res = Reservation.objects.get(pk=self.res.pk)
        self.assertFalse(res.is_confirmed())
