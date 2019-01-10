from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from core.form import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'base_form.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UpdateUser(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('pilot', kwargs={'pk': self.request.user.pilot.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return redirect(self.get_success_url())
