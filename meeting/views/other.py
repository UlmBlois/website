# django
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.utils import timezone as tz
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

import os
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
        context['images'] = os.listdir(
            os.path.join(settings.STATIC_ROOT, "img"))
        return context


@method_decorator(login_required, name='dispatch')
class LoggedIndexView(TemplateView):
    template_name = 'logged_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not self.request.user.pilot.is_complete():
            messages.add_message(self.request, messages.WARNING,
                                 _('str_message_incomplete_profile'))
        return context


class TimeSlotAviableView(TemplateView):
    anonymous_template_name = 'aviable_timeslot.html'
    logged_template_name = 'aviable_timeslot_logged.html'

    def get_template_names(self):
        name = self.anonymous_template_name
        if self.request.user.is_authenticated:
            name = self.logged_template_name
        return [name]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        meeting = Meeting.objects.active()
        context['meeting'] = meeting
        if(meeting):
            days = meeting.open_days()
            delta = timedelta(days=1)
            slots_by_days = []
            for d in days:
                start_d = tz.make_aware(
                    datetime.combine(d, datetime.min.time()))
                slots_by_days.append(
                    list(meeting.timeslot_set.filter(
                            start_date__gte=start_d,
                            start_date__lt=start_d+delta
                            ).order_by('start_date')))
            context['ts_table'] = [days] + list(zip_longest(*slots_by_days))
            context['ts_aviables'] = TimeSlot.objects.aviables()
            departures = TimeSlot.objects.departures_slots_left()
            context['ts_departures_aviables'] = departures
        return context


class ReservationConfirmationEmail(TemplateView):
    template_name = 'emails/reservation_confirmation_request.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['browser_url'] = 'reservation_confirmation_email'
        return context
