from django.test import TestCase
from django.utils import timezone as tz

from datetime import date, datetime

from meeting.tests.utils import (create_meeting, create_time_slot,
                                 PermissionRequiredTestCase, create_user)


# TODO FINISH
class MeetingStatsView(PermissionRequiredTestCase, TestCase):
    url = '/meeting/chart/meeting'
    url_name = 'meeting_stat'
    template_name = 'meeting_statistic.html'
    permission_required = ['reservation_validation']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
