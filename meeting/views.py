from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import (UpdateView, DeleteView, CreateView,
                                       FormMixin, ProcessFormView)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django_filters.views import FilterView
from django.contrib.auth.models import User
from meeting.models import Pilot, ULM, Reservation
from meeting.form import (ReservationForm, UserEditMultiForm,
                          AjaxFuelServedForm, ULMForm, StaffReservationEditForm)
import uuid


# TODO: tmp
def index(request):
    """View function for the reservation list."""
    num_res = Reservation.objects.count()
    res_list = Reservation.objects.all()

    context = {
        'num_res': num_res,
        'res_list': res_list,
    }
    return render(request, 'index.html', context=context)


class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context

###########################################################################from django.views.generic.edit import FormMixin, ProcessFormView####
# STAFF related View
###############################################################################


class FilteredReservationList(UserPassesTestMixin, PaginatedFilterViews,
                              FilterView):
    model = Reservation
    paginate_by = 2

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(time_slot__meeting__active=True).order_by(
            '-reservation_number')


###############################################################################
# PILOT related View
###############################################################################


def pilot_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base_form.html', {
        'form': form
    })


@method_decorator(login_required, name='dispatch')
class DetailPilot(DetailView):
    model = Pilot
    pk_url_kwarg = 'pk'
    context_object_name = 'pilot'
    template_name = 'pilot_profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

    def get_object(self, queryset=None):
        obj = super(DetailPilot, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


@method_decorator(login_required, name='dispatch')
class UpdateUserPilotView(UpdateView):
    model = User
    pk_url_kwarg = 'pk'
    form_class = UserEditMultiForm
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.kwargs.get('pk', None)})

    def get_form_kwargs(self):
        kwargs = super(UpdateUserPilotView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'pilot': self.object.pilot,
        })
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk', None))

    def get_object(self, queryset=None):
        obj = super(UpdateUserPilotView, self).get_object()
        if not obj == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        form['user'].save()
        pilot = form['pilot'].save(commit=False)
        pilot.last_update = timezone.now()
        pilot.save()
        return redirect(self.get_success_url())


###############################################################################
# ULM related View
###############################################################################

@method_decorator(login_required, name='dispatch')
class PilotULMList(ListView):
    model = ULM
    context_object_name = 'ulm_list'
    template_name = 'pilot_ulm_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.request.user.pilot).order_by(
            '-imatriculation')


@method_decorator(login_required, name='dispatch')
class DeletePilotULM(DeleteView):
    model = ULM
    template_name = 'ulm_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(DeletePilotULM, self).get_object()
        if not obj.pilot == self.request.user.pilot:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('pilot_ulm_list')


@method_decorator(login_required, name='dispatch')
class CreatePilotULM(CreateView):
    model = ULM
    fields = [
             'constructor', 'model', 'type', 'imatriculation_country',
             'imatriculation', 'radio_id']
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot_ulm_list')

    def form_valid(self, form):
        model = form.save(commit=False)
        model.pilot = self.request.user.pilot
        model.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class UpdatePilotULM(UpdateView):
    model = ULM
    fields = [
        'constructor', 'model', 'imatriculation_country',
        'imatriculation', 'radio_id'
        ]
    pk_url_kwarg = 'pk'
    context_object_name = 'ulm'
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot_ulm_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.request.user.pilot)

    def form_valid(self, form):
        ulm = form.save(commit=False)
        ulm.save()
        return redirect(self.get_success_url())

###############################################################################
# ULM related View
###############################################################################


@method_decorator(login_required, name='dispatch')
class PilotReservationList(ListView):
    model = Reservation
    context_object_name = 'reservation_list'
    template_name = 'pilot_reservation_list.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(ulm__pilot=self.request.user.pilot).order_by(
            '-reservation_number')


@method_decorator(login_required, name='dispatch')
class CreatePilotReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot_reservation')

    def get_form_kwargs(self):
        kwargs = super(CreatePilotReservation, self).get_form_kwargs()
        kwargs.update({'pilot': self.request.user.pilot})
        return kwargs

    def form_valid(self, form):
        uuid.uuid4().hex[:6].upper()
        res = form.save(commit=False)
        key = uuid.uuid4().hex[:6].upper()
        while Reservation.objects.filter(reservation_number=key).exists():
            key = uuid.uuid4().hex[:6].upper()
        res.reservation_number = key
        res.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class UpdatePilotReservation(UpdateView):
    model = Reservation
    form_class = ReservationForm
    pk_url_kwarg = 'pk'
    context_object_name = 'reservation'
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot_reservation')

    def get_form_kwargs(self):
        kwargs = super(UpdatePilotReservation, self).get_form_kwargs()
        kwargs.update({'pilot': self.request.user.pilot})
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(ulm__pilot=self.request.user.pilot)

    def form_valid(self, form):
        res = form.save(commit=False)
        res.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class DeletePilotReservation(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(DeletePilotReservation, self).get_object()
        if not obj.ulm.pilot == self.request.user.pilot:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('pilot_reservation')


###############################################################################
# Ajax View
###############################################################################

def save_reservation_form(request, form, template_name, additional_context={}):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    context.update(additional_context)
    data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)


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

def ajax_staff_edit_reservation(request, pk):
    data = {}
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = StaffReservationEditForm(request.POST, reservation=reservation)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = StaffReservationEditForm(reservation=reservation)
    return save_reservation_form(request, form, 'staff_reservation_edit_partial.html', additional_context={'reservation': reservation})

def ajax_load_pilot_ulm_list(request):
        pilot_pk = request.GET.get('pilot')
        ulm_list = ULM.objects.filter(pilot__pk=pilot_pk).order_by(
            '-immatriculation')
        return render(request, 'pilot_ulm_list_dropdown.html',
                      {'list': ulm_list})
