from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Permission

from datetime import timedelta
import logging
from meeting.models import Meeting, TimeSlot, Reservation, ULM

logger = logging.getLogger(__name__)


def create_meeting(name, start_date, active):
    end_date = start_date + timedelta(days=2)
    registration_start = start_date - timedelta(days=60)
    registration_end = start_date - timedelta(days=5)
    return Meeting.objects.create(
            name=name,
            active=active,
            start_date=start_date,
            end_date=end_date,
            registration_start=registration_start,
            registration_end=registration_end)


def create_time_slot(meeting, start_date, arrivals_slots, end_date=None):
    if end_date is None:
        end_date = start_date + timedelta(minutes=30)
    return TimeSlot.objects.create(meeting=meeting,
                                   start_date=start_date,
                                   end_date=end_date,
                                   arrivals_slots=arrivals_slots)


def create_ulm(pilot, radio_id):
    return ULM.objects.create(pilot=pilot,
                              radio_id=radio_id,
                              )


def create_user(name, password):
    return User.objects.create_user(username=name, password=password)


def create_reservation(res_num, ulm, ts1, ts2=None, arrival=None):
    return Reservation.objects.create(
                ulm=ulm,
                pilot=ulm.pilot,
                reservation_number=res_num,
                time_slot=ts1,
                arrival=arrival,
                depart_time_slot=ts2,
                meeting=ts1.meeting)


class ViewTestCase(object):
    url = ''
    url_name = ''
    template_name = ''

    def get_url(self):
        return self.url

    def get_url_from_name(self, args=None, kwargs=None):
        return reverse(self.url_name, args=args, kwargs=kwargs)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.get_url_from_name())
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        if self.template_name != '':
            response = self.client.get(self.get_url())
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, self.template_name)


class LoggedViewTestCase(ViewTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user("user", "testtest")

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        super().test_view_url_exists_at_desired_location()

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        super().test_view_url_accessible_by_name()

    def test_template(self):
        self.client.force_login(self.user)
        super().test_template()

    def test_login_required(self):
        response = self.client.get(self.get_url())
        redirect = reverse('login') + "?next=" + self.get_url()
        self.assertRedirects(response, redirect)


class PermissionRequiredTestCase(LoggedViewTestCase):
    permission_required = []

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        permissions = Permission.objects.get(
            codename__in=cls.permission_required)
        cls.user.user_permissions.add(permissions)
        # create an unauthorizes user
        cls.user2 = create_user('user2', 'testtest')

    def test_unauthorized_access(self):
        self.client.force_login(self.user2)
        # with self.assertRaises(PermissionDenied):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 403)
