# django
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string
# owned
from meeting.models import Reservation
from .utils import save_reservation_form
from meeting.form import AjaxFuelServedForm, ULMForm
from meeting.models import ULM, Pilot


def ajax_fuel_served(request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        if request.method == 'POST':
            form = AjaxFuelServedForm(request.POST, instance=reservation)
        else:
            form = AjaxFuelServedForm(instance=reservation)
        return save_reservation_form(request, form,
                                     'reservation_fuel_served_update.html')


def ajax_load_pilot_ulm_list(request):
        pilot_pk = request.GET.get('pilot')
        ulm_list = ULM.objects.filter(pilot__pk=pilot_pk).order_by(
            '-immatriculation')
        return render(request, 'pilot_ulm_list_dropdown.html',
                      {'list': ulm_list})


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
