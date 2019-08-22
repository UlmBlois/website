# django
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required

# owned
from meeting.models import Reservation
from .utils import save_reservation_form

from meeting.form import AjaxFuelServedForm

# TODO add permissions
@login_required
def ajax_fuel_served(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = AjaxFuelServedForm(request.POST, instance=reservation)
    else:
        form = AjaxFuelServedForm(instance=reservation)
    return save_reservation_form(request, form,
                                 'reservation_fuel_served_update.html')


# TODO call with ajax and make the appropriate change to the view and the template
# FIXME: Security breach user can acces Reservation of other users
@login_required
def ajax_pilot_cancel_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.cancel()
    res.save()
    return HttpResponseRedirect(reverse('pilot_reservation'))


# TODO call with ajax and make the appropriate change to the view and the template
# FIXME: Security breach user can acces Reservation of other users
@login_required
def ajax_pilot_confirm_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.confirm()
    res.save()
    return redirect(reverse('pilot_reservation'))


# TODO add permissions
@login_required
def ajax_staff_cancel_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.cancel()
    res.save()
    return HttpResponseRedirect(reverse('staff_reservation_overview',
                                        kwargs={'pk': pk}))


# TODO add permissions
@login_required
def ajax_staff_confirm_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.confirm()
    res.save()
    return redirect(reverse('staff_reservation_overview', kwargs={'pk': pk}))
