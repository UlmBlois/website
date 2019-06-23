from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.utils import timezone

from datetime import date, datetime, timedelta
from unittest import skip
import logging
from meeting.models import Meeting, TimeSlot, Pilot, Reservation, ULM

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
