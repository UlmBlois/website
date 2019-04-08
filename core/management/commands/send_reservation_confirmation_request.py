from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from datetime import date
from meeting.models import Reservation, Meeting


class Command(BaseCommand):
    help = _('Send an email asking users to confirm their reservation (active '
             'meeting only). The email will be sent only if on the specified '
             'date in the meeting settings.')
    email_template = ''

    def handle(self, *args, **kwargs):
        meeting = Meeting.objects.active()
        if meeting.confirmation_reminder_date == date.today():
            unconfirmed_res = Reservation.objects.unconfirmed_actives()
            email_list = [x.ulm.pilot.user.email for x in unconfirmed_res
                          if x.ulm is not None and x.ulm.pilot is not None]
            for email in email_list:
                self.stdout.write(email)  # TODO send email

        else:
            self.stdout.write("Nothing to do")
