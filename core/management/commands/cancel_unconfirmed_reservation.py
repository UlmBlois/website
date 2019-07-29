from django.core.management.base import BaseCommand
from meeting.models import Reservation, Meeting
from datetime import timedelta, date
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-n',
            '--now',
            action='store_true',
            help='Cancel unconfirmed reservation imediatly, '
                 'without regard of the timeline.'
                 'Default is meeting.automatic_cancelation_date',
        )

    def handle(self, *args, **options):
        logger.debug("Start Cancel_unconfirmed_reservation command.")
        meeting = Meeting.objects.active()
        cancel_date = meeting.start_date - timedelta(days=3)
        if options['now'] or cancel_date == date.today():
            unconfirmed_res = Reservation.objects.unconfirmed_actives()
            nb_unconfirmed = len(unconfirmed_res)
            unconfirmed_res.update(canceled=True,
                                   confirmed=False,
                                   time_slot=None,
                                   depart_time_slot=None)
            logger.debug('%s unconfirmed reservation have been canceled',
                         nb_unconfirmed)
        else:
            logger.debug('Cancelation planified on %s', str(cancel_date))
        logger.debug("End Cancel_unconfirmed_reservation command.")
