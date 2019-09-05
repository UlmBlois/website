from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from meeting.models import Reservation, Meeting


@method_decorator(login_required, name='dispatch')
class MeetingStatsView(PermissionRequiredMixin, TemplateView):
    template_name = 'meeting_statistic.html'
    permission_required = ('meeting.reservation_validation')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['arrival_by_days'] = self.arrival_by_days()
        return context

    def arrival_by_days(self):
        meeting = Meeting.objects.active()
        arrival_by_days = []
        if(meeting):
            res = Reservation.objects.actives().filter(arrival__isnull=False)
            days = meeting.open_days()
            for d in days:
                arrival_by_days.append((
                    d,
                    res.filter(arrival__year=d.year,
                               arrival__month=d.month,
                               arrival__day=d.day).count()))
        return arrival_by_days
