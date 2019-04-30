from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from datetime import date
from meeting.models import Reservation, Meeting


class Command(BaseCommand):
    help = _('Send an email asking users to confirm their reservation (active '
             'meeting only). The email will be sent only if on the specified '
             'date in the meeting settings.')
    email_template = 'reservation_confirmation_request.html'

    def handle(self, *args, **kwargs):
        meeting = Meeting.objects.active()
        subject = _("Confirm your reservation")
        from_email = 'noreply@salon-ulm-blois.fr'
        context = {'meeting': meeting}
        message = render_to_string(self.email_template, context=context)
        email_pack = []
        if meeting.confirmation_reminder_date == date.today():
            unconfirmed_res = Reservation.objects.unconfirmed_actives()
            email_list = [x.pilot.user.email for x in unconfirmed_res
                          if x.ulm is not None and x.pilot is not None]
            for email in email_list:
                email_pack.append((subject, message, from_email, [email]))
                # self.stdout.write(email)  # TODO send email
            send_mass_mail(email_pack, fail_silently=False)
        else:
            self.stdout.write("Nothing to do")
