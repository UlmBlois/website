from django.urls import reverse
# from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.utils import timezone as tz

from datetime import timedelta, date, datetime
import logging

from meeting.models import Meeting, TimeSlot, Reservation, ULM


logger = logging.getLogger(__name__)


def fill_pilot(pilot):
    pilot.insurance_company = "insurer"
    pilot.insurance_number = "123A"
    pilot.licence_number = "111"
    pilot.phone_number = "+33678451289"
    pilot.street_name = "street"
    pilot.city = "city"
    pilot.city_code = "12453"


def create_meeting(name, start_date, active=True):
    end_date = start_date + timedelta(days=2)
    registration_start = start_date - timedelta(days=60)
    registration_end = start_date - timedelta(days=5)
    return Meeting.objects.create(
            name=name,
            active=active,
            start_date=start_date,
            end_date=end_date,
            registration_start=registration_start,
            registration_end=registration_end,
            confirmation_reminder_date=registration_end)


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


def create_user(name, password, email=""):
    if email == "":
        email = name + "@test.fr"
    return get_user_model().objects.create_user(
        username=name, password=password, email=email)


def create_reservation(res_num, ulm, ts1, ts2=None, arrival=None,
                       confirmed=False, canceled=False, fuel_reservation=0):
    return Reservation.objects.create(
                ulm=ulm,
                pilot=ulm.pilot,
                reservation_number=res_num,
                time_slot=ts1,
                arrival=arrival,
                depart_time_slot=ts2,
                meeting=ts1.meeting,
                confirmed=confirmed,
                canceled=canceled,
                fuel_reservation=fuel_reservation)


def create_full_reservation(res_num=None, user=None, ulm=None, meeting=None,
                            ts1=None, ts2=None, confirmed=False,
                            canceled=False, arrival=None):
    if meeting is None:
        meeting = create_meeting("1", date(2019, 8, 30), True)
    if ts1 is None:
        ts1 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 10)),
                               5)
    if ts2 is None:
        ts2 = create_time_slot(meeting,
                               tz.make_aware(datetime(2019, 8, 31, 11)),
                               5)
    if user is None and ulm is None:
        user = create_user('testuser', '12345')
    elif user is None and ulm is not None:
        user = ulm.pilot.user
    if ulm is None:
        ulm = create_ulm(user.pilot, 'F-JLOV')
    if res_num is None:
        res_num = 'FAE1F6'
    return create_reservation(res_num, ulm, ts1, ts2,
                              arrival, confirmed, canceled)


class ViewTestCase(object):
    url = ''
    url_name = ''
    template_name = ''
    redirect_url_name = ''

    def get_redirect_url(self, args=None, kwargs=None):
        return reverse(self.redirect_url_name, args=args, kwargs=kwargs)

    def get_url(self):
        return self.url

    def get_url_from_name(self, args=None, kwargs=None):
        return reverse(self.url_name, args=args, kwargs=kwargs)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.get_url())
        if self.redirect_url_name != '':
            self.assertRedirects(response, self.get_redirect_url())
        else:
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.get_url_from_name())
        if self.redirect_url_name != '':
            self.assertRedirects(response, self.get_redirect_url())
        else:
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
