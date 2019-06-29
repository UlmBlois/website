# django
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
# owned
from meeting.models import Meeting


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['meeting'] = Meeting.objects.active()
        return context


@method_decorator(login_required, name='dispatch')
class LoggedIndexView(TemplateView):
    template_name = 'logged_index.html'


# TODO: Test View to remove
class BaseEmailView(TemplateView):
    template_name = 'emails/base_email.html'


# TODO: Test View to remove
class ReservationConfirmationEmail(TemplateView):
    template_name = 'emails/reservation_confirmation_request.html'
