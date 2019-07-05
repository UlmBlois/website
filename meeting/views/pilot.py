# django
from django.shortcuts import redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import (UpdateView, DeleteView, CreateView,)
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
# python
import uuid
import logging

# Third party
from extra_views import ModelFormSetView
# owned
from meeting.models import Pilot, ULM, Reservation, Meeting
from meeting.form import (ReservationForm, UserEditMultiForm,
                          ULMForm, ULMFormSetHelper, BaseULMForm,
                          PilotPasswordChangeForm)
from meeting.views.utils import PAGINATED_BY

logger = logging.getLogger(__name__)


# TODO: move this view to Core?
@method_decorator(login_required, name='dispatch')
class PilotChangePassword(FormView):
    form_class = PilotPasswordChangeForm
    template_name = 'base_logged_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.request.user.pilot.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, self.request.user)  # Important!
        messages.add_message(self.request, messages.INFO,
                             _('str_message_password_updated'))
        return super().form_valid(form)


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
        form['pilot_form'].save()
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
    template_name = 'logged_delete_form.html'
    # Translators: This contain the ulm name acces by %(ulm)s
    success_message = _("str_message_ulm_deleted")
    # Translators: This contain the ulm name acces by %(ulm)s
    error_message = _('str_message_delete_ulm_link_to_reservation')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = reverse('pilot_ulm_list')
        return context

    def get_object(self, queryset=None):
        obj = super(DeletePilotULM, self).get_object()
        if not obj.pilot == self.request.user.pilot:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('pilot_ulm_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.reservations.actives().filter(canceled=False):
            messages.error(
                self.request,
                self.error_message % {'ulm': obj.radio_id})
            return redirect(reverse('pilot_ulm_list'))
        else:
            messages.success(
                self.request,
                self.success_message % {'ulm': obj.radio_id})
            return super().delete(request, *args, **kwargs)


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
# Reservation related View
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
        res = form.save(commit=False)
        key = uuid.uuid4().hex[:6].upper()
        while Reservation.objects.filter(reservation_number=key).exists():
            key = uuid.uuid4().hex[:6].upper()
        res.reservation_number = key
        res.meeting = res.time_slot.meeting
        res.pilot = res.ulm.pilot
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


###############################################################################
# Reservation wizard
###############################################################################

@method_decorator(login_required, name='dispatch')
class ReservationWizardStep1(UpdateUserPilotView):

    def get_success_url(self):
        return reverse('reservation_wizard_step2',
                       kwargs={'pilot': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ReservationWizardStep2(ModelFormSetView):
    pilot = None
    model = ULM
    form_class = BaseULMForm
    template_name = 'base_logged_form.html'
    factory_kwargs = {'extra': 1}

    def get_success_url(self):
        return reverse('pilot_create_reservation')

    def get_queryset(self):
        self.pilot = self.kwargs.get('pilot', None)
        queryset = super().get_queryset()
        return queryset.filter(pilot=self.pilot)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        helper = ULMFormSetHelper()
        helper.form_tag = False
        context['helper'] = helper
        return context

    def get_initial(self):
        # Get a list of initial values for the formset here
        initial = [{'pilot': self.kwargs.get('pilot', None)}]
        return initial

    def formset_valid(self, formset):
        """
        If the formset is valid redirect to the supplied URL
        """
        for form in formset:
            ulm = form.save(commit=False)
            if not ulm.radio_id == '':
                ulm.pilot = Pilot.objects.get(pk=self.pilot)
                ulm.save()
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        """
        If the formset is invalid, re-render the context data with the
        data-filled formset and errors.
        """
        logger.debug("formset " + str(len(formset)))

        for form in formset:
            logger.debug("form is valid: " + str(form.is_valid()))
            logger.debug(str(form.cleaned_data))
            logger.debug(form.errors)
        return self.render_to_response(self.get_context_data(formset=formset))
