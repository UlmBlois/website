from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django_filters.views import FilterView
from meeting.models import Pilot, ULM, Reservation
from meeting.form import ReservationForm
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

###############################################################################
# STAFF related View
###############################################################################


class FilteredList(UserPassesTestMixin, PaginatedFilterViews, FilterView):
    model = Reservation
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff


class StaffReservationList(UserPassesTestMixin, ListView):
    model = Reservation  # TODO a finir
    context_object_name = 'reservation_list'
    template_name = 'staff_reservation_list.html'
    paginate_by = 2

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(time_slot__meeting__active=True).order_by(
            '-time_slot__start_date')


class StaffFuelReservationList(UserPassesTestMixin, ListView):
    model = Reservation  # TODO a finir
    context_object_name = 'reservation_list'
    template_name = 'staff_fuel_reservation_list.html'
    paginate_by = 2

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
                              time_slot__meeting__active=True,
                              fuel_reservation__gt=0).order_by(
                              '-time_slot__start_date')
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
        return queryset.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class UpdatePilot(UpdateView):
    model = Pilot
    fields = [
             'insurance_number', 'insurance_file',
             'licence_number', 'licence_file']
    # pk_url_kwarg = 'pk'
    # context_object_name = 'pilot'
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.request.user.pilot.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        pilot = form.save(commit=False)
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
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.request.user.pilot)


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
             'constructor', 'model', 'imatriculation_country',
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
        return queryset.filter(ulm__pilot=self.request.user.pilot)


@method_decorator(login_required, name='dispatch')
class CreatePilotReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot_reservation')

    def get_form_kwargs(self):
        kwargs = super(CreatePilotReservation, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
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
        kwargs.update({'user': self.request.user})
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
