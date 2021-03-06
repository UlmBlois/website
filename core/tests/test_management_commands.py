from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from django.utils.six import StringIO
from datetime import date
from unittest.mock import patch

from freezegun import freeze_time

from meeting.models import Reservation
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
    def test_command_D_day_no_batch(self):
        call_command('send_reservation_confirmation_request')
        self.assertEqual(len(mail.outbox), 2)

    @freeze_time('2019-08-25')
    def test_command_D_day_batch(self):
        out = StringIO()
        call_command('send_reservation_confirmation_request',
                     batch=1, stdout=out)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('batch number: 2/2', out.getvalue())

    @freeze_time('2019-08-25')
    def test_command_D_day_batch_interval(self):
        out = StringIO()
        with patch('time.sleep', return_value=None):
            call_command('send_reservation_confirmation_request',
                         batch=1,
                         interval=30,
                         stdout=out)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('batch number: 2/2', out.getvalue())

    @freeze_time('2019-07-30')
    def test_command_wrong_day(self):
        call_command('send_reservation_confirmation_request')
        self.assertEqual(len(mail.outbox), 0)


class CancelUnconfirmedReservationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        meeting = create_meeting("1", date(2019, 8, 30), True)
        user1 = create_user('user1', '12345')
        user2 = create_user('user2', '12345')
        user3 = create_user('user3', '12345')
        res1 = create_full_reservation(res_num='FAE1F6', user=user1,
                                       meeting=meeting)
        res2 = create_full_reservation(res_num='FAE1F7', user=user2,
                                       meeting=meeting)
        create_full_reservation(res_num='FAE1F8', user=user3,
                                meeting=meeting, confirmed=True)
        cls.unconfirmed = [res1, res2]

    @freeze_time('2019-08-27')
    def test_command_D_day(self):
        call_command('cancel_unconfirmed_reservation')
        unconfirmed_actives = Reservation.objects.unconfirmed_actives()
        self.assertQuerysetEqual(unconfirmed_actives,
                                 [],
                                 ordered=False)

    @freeze_time('2019-08-10')
    def test_command_wrong_day(self):
        call_command('cancel_unconfirmed_reservation')
        unconfirmed_actives = Reservation.objects.unconfirmed_actives()
        self.assertQuerysetEqual(unconfirmed_actives,
                                 [repr(x) for x in self.unconfirmed],
                                 ordered=False)

    @freeze_time('2019-08-10')
    def test_command_now(self):
        call_command('cancel_unconfirmed_reservation', '--now')
        unconfirmed_actives = Reservation.objects.unconfirmed_actives()
        self.assertQuerysetEqual(unconfirmed_actives,
                                 [],
                                 ordered=False)
