# django
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

# owned
from meeting.models import Reservation
from .utils import save_reservation_form

from meeting.form import AjaxFuelServedForm


def ajax_fuel_served(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = AjaxFuelServedForm(request.POST, instance=reservation)
    else:
        form = AjaxFuelServedForm(instance=reservation)
    return save_reservation_form(request, form,
                                 'reservation_fuel_served_update.html')


# TODO call with ajax and make the appropriate change to the view and the template
def ajax_cancel_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.canceled = True
    res.time_slot = None
    res.depart_time_slot = None
    res.confirmed = False
    res.save()
    print(res)
    return HttpResponseRedirect(reverse('pilot_reservation'))


# TODO call with ajax and make the appropriate change to the view and the template
def ajax_confirm_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if not res.canceled:
        res.confirmed = True
    res.save()
    return redirect(reverse('pilot_reservation'))
