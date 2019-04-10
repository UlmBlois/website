# django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
# owned
from meeting.models import Reservation, Meeting


def index(request):
    """View function for the reservation list."""
    num_res = Reservation.objects.count()
    res_list = Reservation.objects.all()
    meeting = Meeting.objects.active()
    context = {
        'num_res': num_res,
        'res_list': res_list,
        'meeting': meeting,
    }
    return render(request, 'index.html', context=context)


@method_decorator(login_required, name='dispatch')
class LoggedIndexView(TemplateView):
    template_name = 'logged_index.html'
