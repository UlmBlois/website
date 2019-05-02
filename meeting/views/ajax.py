# django
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
# owned
from meeting.models import Reservation
from .utils import save_reservation_form

from meeting.form import AjaxFuelServedForm, ULMForm
from meeting.models import Pilot


def ajax_fuel_served(request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        if request.method == 'POST':
            form = AjaxFuelServedForm(request.POST, instance=reservation)
        else:
            form = AjaxFuelServedForm(instance=reservation)
        return save_reservation_form(request, form,
                                     'reservation_fuel_served_update.html')


def ajax_add_ulm(request, pk):
    data = {}
    if request.method == 'POST':
        form = ULMForm(request.POST)
        if form.is_valid():
            ulm = form.save(commit=False)
            ulm.pilot = get_object_or_404(Pilot, pk=pk)
            ulm.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ULMForm()
    context = {'form': form}
    context.update({'pilot': pk})
    data['html_form'] = render_to_string('add_pilot_ulm.html',
                                         context, request=request)
    return JsonResponse(data)


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
