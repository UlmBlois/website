from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import date
from meeting.models import Reservation, Meeting
import logging
import time

logger = logging.getLogger(__name__)


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


class Command(BaseCommand):
    # Translators: optional
    help = _('str_Helptext_send_resevation_conifirmation_request')
    email_template = 'reservation_confirmation_request.html'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-b',
            '--batch',
            action='store',
            nargs='?',
            type=int,
            default=0,
            help='Number of email send per batch (default: 0=all)',
        )
        parser.add_argument(
            '-i',
            '--interval',
            action='store',
            nargs='?',
            type=int,
            default=0,
            help='Interval in minutes between email batch (default: 0)',
        )
        parser.add_argument(
            '-n',
            '--now',
            action='store_true',
            help='Send confirmation request email imediatly',
        )

    def handle(self, *args, **options):
        meeting = Meeting.objects.active()

        if options['now'] or meeting.confirmation_reminder_date == date.today():
            subject = _("str_Confirmation_Reminder_Email_Subject")
            context = {
                'meeting': meeting,
                'browser_url': 'reservation_confirmation_email'}
            message = render_to_string(self.email_template, context=context)
            email_pack = []
            unconfirmed_res = Reservation.objects.unconfirmed_actives()
            email_list = [x.pilot.user.email for x in unconfirmed_res
                          if x.ulm is not None and x.pilot is not None]

            for email in email_list:
                email_pack.append((subject, strip_tags(message), message,
                                   None, [email]))

            logger.debug("send confirmation reminder to: %i", len(email_list))

            batch_email = [email_pack]
            if options['batch'] > 0:
                n = options['batch']
                batch_email = [email_pack[i * n:(i + 1) * n] for i in
                               range((len(email_pack) + n - 1) // n)]

            for i, batch in enumerate(batch_email):
                send_mass_html_mail(batch, fail_silently=False)

                logger.debug('batch number: %s/%s, of size: %s',
                             i+1, len(batch_email), len(batch))
                self.stdout.write(
                    'batch number: %s/%s' % (i+1, len(batch_email)))
                self.stdout.write('batch size: %s' % len(batch))

                if options['interval'] > 0:
                    time.sleep(60*options['interval'])
        else:
            logger.debug("No reminder to send today next one on : %s",
                         str(meeting.confirmation_reminder_date))
