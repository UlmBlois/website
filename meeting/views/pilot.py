# django
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import (UpdateView, DeleteView, CreateView,)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import logging
# python
import uuid
# Third party
from formtools.wizard.views import SessionWizardView
# owned
from meeting.models import Pilot, ULM, Reservation, Meeting
from meeting.form import (ReservationForm, UserEditMultiForm,
                          ULMForm, UlmFormSet, PilotForm, UserEditForm)
from meeting.views.utils import PAGINATED_BY

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
def pilot_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             _('Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
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
    model = Pilot
    pk_url_kwarg = 'pk'
    form_class = UserEditMultiForm
    template_name = 'base_logged_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(UpdateUserPilotView, self).get_form_kwargs()
        kwargs.update(instance={
            'user_form': self.object.user,
            'pilot_form': self.object,
        })
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk', None))

    def get_object(self, queryset=None):
        obj = super(UpdateUserPilotView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        form['user_form'].save()
        pilot = form['pilot_form'].save(commit=False)
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
    paginate_by = PAGINATED_BY

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
    form_class = ULMForm
    template_name = 'base_logged_form.html'

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
    form_class = ULMForm
    pk_url_kwarg = 'pk'
    context_object_name = 'ulm'
    template_name = 'base_logged_form.html'

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
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.request.user.pilot).order_by(
            '-reservation_number')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['meeting'] = Meeting.objects.active()
        return context


@method_decorator(login_required, name='dispatch')
class CreatePilotReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'base_logged_form.html'

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
        res.pilot = res.ulm.pilot
        res.meeting = res.time_slot.meeting
        res.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class UpdatePilotReservation(UpdateView):
    model = Reservation
    form_class = ReservationForm
    pk_url_kwarg = 'pk'
    context_object_name = 'reservation'
    template_name = 'base_logged_form.html'

    def get_success_url(self):
        return reverse('pilot_reservation')

    def get_form_kwargs(self):
        kwargs = super(UpdatePilotReservation, self).get_form_kwargs()
        kwargs.update({'pilot': self.request.user.pilot})
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.request.user.pilot)

    def form_valid(self, form):
        res = form.save(commit=False)
        res.canceled = False
        res.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class DeletePilotReservation(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(DeletePilotReservation, self).get_object()
        if not obj.pilot == self.request.user.pilot:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('pilot_reservation')


@method_decorator(login_required, name='dispatch')
class MakeReservationWizard(SessionWizardView):
    template_name = 'base_logged_wizard_form.html'
    form_list = [('pilot', PilotForm), ('ulm', UlmFormSet)]

    def get_success_url(self):
        return reverse('pilot_reservation')

    def done(self, form_list, form_dict, **kwargs):
        # pilot = form_dict['pilot'].save()
        # ulms = form_dict['ulms'].save()
        # res = form_dict['reservation'].save(commit=False)
        # key = uuid.uuid4().hex[:6].upper()
        # while Reservation.objects.filter(reservation_number=key).exists():
        #     key = uuid.uuid4().hex[:6].upper()
        # res.reservation_number = key
        # res.pilot = res.ulm.pilot
        # res.meeting = res.time_slot.meeting
        # res.save()
        return HttpResponseRedirect(self.get_success_url())

        def get_form_instance(self, step):
            logger.debug('get form instance for ' + step )
            if step == 'pilot':
                self.instance = Pilot.objects.get(user=self.request.user.pk)
                logger.debug(self.instance)
            if step == 'ulm':
                self.instance = ULM.objects.filter(pilot=self.request.user.pilot.pk)
            return self.instance
    # def process_step(self, form):
        # model = form.save(commit=False)
        # model.save()
        # return self.get_form_step_data(form)
