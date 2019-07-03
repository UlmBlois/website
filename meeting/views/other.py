# django
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.utils import timezone as tz

from datetime import datetime, timedelta
from itertools import zip_longest
import logging
# owned
from meeting.models import Meeting, TimeSlot

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['meeting'] = Meeting.objects.active()
        return context


@method_decorator(login_required, name='dispatch')
class LoggedIndexView(TemplateView):
    template_name = 'logged_index.html'


class TimeSlotAviableView(TemplateView):
    template_name = 'aviable_timeslot.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        meeting = Meeting.objects.active()
        context['meeting'] = meeting
        days = meeting.open_days()
        delta = timedelta(days=1)
        slots_by_days = []
        for d in days:
            start_d = tz.make_aware(datetime.combine(d, datetime.min.time()))
            slots_by_days.append(
                list(meeting.timeslot_set.filter(
                        start_date__gte=start_d,
                        start_date__lt=start_d+delta).order_by('start_date')))
        context['ts_table'] = [days] + list(zip_longest(*slots_by_days))
        context['ts_aviables'] = TimeSlot.objects.aviables()
        return context


# TODO: Test View to remove
class BaseEmailView(TemplateView):  # pragma: no cover
    template_name = 'emails/base_email.html'


# TODO: Test View to remove
class ReservationConfirmationEmail(TemplateView):  # pragma: no cover
    template_name = 'emails/reservation_confirmation_request.html'
