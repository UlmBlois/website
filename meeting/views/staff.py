# django
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.utils import timezone
# third party
from django_filters.views import FilterView
# owned
from .utils import PaginatedFilterViews, PAGINATED_BY
from meeting.models import Pilot, ULM, Reservation
from meeting.form import (ReservationForm, UserEditMultiForm, ULMForm)

import logging

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class PilotOverview(PermissionRequiredMixin, DetailView):
    model = Pilot
    pk_url_kwarg = 'pk'
    context_object_name = 'pilot'
    template_name = 'pilot_summary.html'
    permission_required = ('meeting.reservation_validation')


@method_decorator(login_required, name='dispatch')
class StaffUpdatePilot(PermissionRequiredMixin, UpdateView):
    model = Pilot
    pk_url_kwarg = 'pk'
    form_class = UserEditMultiForm
    template_name = 'base_logged_form.html'
    permission_required = ('meeting.reservation_validation')

    def get_success_url(self):
        pk = self.kwargs.get('pk', None)
        return reverse('pilot_overview',
                       kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'user_form': self.object.user,
            'pilot_form': self.object,
        })
        return kwargs

    def form_valid(self, form):
        form['user_form'].save()
        form['pilot_form'].save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class StaffReservationUpdatePilot(StaffUpdatePilot):
    model = Pilot
    pk_url_kwarg = 'pk'
    form_class = UserEditMultiForm
    template_name = 'base_logged_form.html'
    permission_required = ('meeting.reservation_validation')

    def get_success_url(self):
        res_pk = self.kwargs.get('res', None)
        return reverse('staff_reservation_overview',
                       kwargs={'pk': res_pk})


@method_decorator(login_required, name='dispatch')
class StaffUpdatePilotULM(PermissionRequiredMixin, UpdateView):
    model = ULM
    form_class = ULMForm
    pk_url_kwarg = 'pk'
    context_object_name = 'ulm'
    template_name = 'base_logged_form.html'
    permission_required = ('meeting.reservation_validation')

    def get_success_url(self):
        pilot_pk = self.kwargs.get('pilot', None)
        return reverse('pilot_overview',
                       kwargs={'pk': pilot_pk})

    def form_valid(self, form):
        ulm = form.save(commit=False)
        ulm.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class StaffReservationUpdatePilotULM(StaffUpdatePilotULM):

    def get_success_url(self):
        res_pk = self.kwargs.get('res', None)
        return reverse('staff_reservation_overview',
                       kwargs={'pk': res_pk})


@method_decorator(login_required, name='dispatch')
class FilteredULMList(PermissionRequiredMixin, PaginatedFilterViews,
                      FilterView):
    model = ULM
    paginate_by = PAGINATED_BY
    permission_required = ('meeting.reservation_validation')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-radio_id')


@method_decorator(login_required, name='dispatch')
class FilteredPilotList(PermissionRequiredMixin, PaginatedFilterViews,
                        FilterView):
    model = Pilot
    paginate_by = PAGINATED_BY
    permission_required = ('meeting.reservation_validation')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-user__first_name')


@method_decorator(login_required, name='dispatch')
class FilteredReservationList(PermissionRequiredMixin, PaginatedFilterViews,
                              FilterView):
    model = Reservation
    paginate_by = PAGINATED_BY
    permission_required = ('meeting.reservation_validation')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(meeting__active=True).order_by(
            '-reservation_number')


@method_decorator(login_required, name='dispatch')
class StaffReservationValidationDetail(PermissionRequiredMixin, DetailView):
    model = Reservation
    pk_url_kwarg = 'pk'
    context_object_name = 'reservation'
    template_name = 'staff_reservation_validation.html'
    permission_required = ('meeting.reservation_validation')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))


@method_decorator(login_required, name='dispatch')
class StaffReservationUpdate(PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    pk_url_kwarg = 'pk'
    context_object_name = 'reservation'
    template_name = 'base_logged_form.html'
    permission_required = ('meeting.reservation_validation')

    def get_success_url(self):
        res_pk = self.kwargs.get(self.pk_url_kwarg, None)
        return reverse('staff_reservation_overview',
                       kwargs={'pk': res_pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'pilot': self.object.pilot})
        return kwargs

    def form_valid(self, form):
        res = form.save(commit=False)
        res.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class StaffUpdatePilotReservation(StaffReservationUpdate):

    def get_success_url(self):
        pilot_pk = self.kwargs.get('pilot', None)
        return reverse('pilot_overview',
                       kwargs={'pk': pilot_pk})


@method_decorator(login_required, name='dispatch')
class StaffReservationValidation(PermissionRequiredMixin, View):
    pk = None
    permission_required = ('meeting.reservation_validation')

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        reservation = get_object_or_404(Reservation, pk=self.pk)
        if reservation.arrival is None:
            reservation.arrival = timezone.now()
            reservation.save()
        return redirect('staff_reservation_overview', pk=self.pk)


@method_decorator(login_required, name='dispatch')
class StaffReservationInvalidation(PermissionRequiredMixin, View):
    pk = None
    permission_required = ('meeting.reservation_validation')

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        reservation = get_object_or_404(Reservation, pk=self.pk)
        reservation.arrival = None
        reservation.save()
        return redirect('staff_reservation_overview', pk=self.pk)
