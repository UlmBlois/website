from django.test import TestCase
from django.core import mail
from django.core.management import call_command

from datetime import date

from freezegun import freeze_time

from meeting.tests.utils import (create_meeting,
                                 create_user, create_full_reservation)


class SendReservationConfirmationRequestTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        user1 = create_user('user1', '12345')
        user2 = create_user('user2', '12345')
        user3 = create_user('user3', '12345')
        create_full_reservation(res_num='FAE1F6', user=user1,
                                meeting=meeting)
        create_full_reservation(res_num='FAE1F7', user=user2,
                                meeting=meeting)
        create_full_reservation(res_num='FAE1F8', user=user3,
                                meeting=meeting, confirmed=True)

    @freeze_time('2019-08-25')
    def test_command_D_day(self):
        call_command('send_reservation_confirmation_request')
        self.assertEqual(len(mail.outbox), 2)

    @freeze_time('2019-07-30')
    def test_command_wrong_day(self):
        call_command('send_reservation_confirmation_request')
        self.assertEqual(len(mail.outbox), 0)
