from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from core.form import SignUpForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('logged_index')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class DeleteUser(DeleteView):
    model = User
    template_name = 'logged_delete_form.html'
    success_message = _("The user %(user)s as been successfully deleted.")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = reverse('pilot',  kwargs={'pk': self.get_object().pk})
        return context

    def get_object(self, queryset=None):
        obj = super(DeleteUser, self).get_object()
        if not obj == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('index')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            self.success_message % {'user': self.get_object()})
        return super().delete(request, *args, **kwargs)


def handler_404(request, exception=None):
    if request.user.is_authenticated:
        return render(request, 'logged_404.html', status=404)
    else:
        return render(request, '404.html', status=404)


def handler_500(request, exception=None):
    if request.user.is_authenticated:
        return render(request, 'logged_500.html', status=500)
    else:
        return render(request, '500.html', status=500)


def handler_403(request, exception=None):
    if request.user.is_authenticated:
        return render(request, 'logged_403.html', status=403)
    else:
        return render(request, '403.html', status=403)


def handler_400(request, exception=None):
    if request.user.is_authenticated:
        return render(request, 'logged_400.html', status=400)
    else:
        return render(request, '400.html', status=400)
