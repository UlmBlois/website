from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from datetime import date
from meeting.models import Reservation, Meeting
import logging

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

    def handle(self, *args, **kwargs):
        meeting = Meeting.objects.active()
        subject = _("str_Confirmation_Reminder_Email_Subject")
        context = {'meeting': meeting}
        message = render_to_string(self.email_template, context=context)
        email_pack = []
        if True or meeting.confirmation_reminder_date == date.today():
            unconfirmed_res = Reservation.objects.unconfirmed_actives()
            email_list = [x.pilot.user.email for x in unconfirmed_res
                          if x.ulm is not None and x.pilot is not None]
            logger.debug("send confirmation reminder to: %i", len(email_list))
            for email in email_list:
                email_pack.append((subject, strip_tags(message), message,
                                   settings.DEFAULT_FROM_EMAIL, [email]))
            send_mass_html_mail(email_pack, fail_silently=False)
        else:
            logger.debug("No reminder to send today next one on : %s",
                         str(meeting.confirmation_reminder_date))
