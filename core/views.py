from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
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
            return redirect('logged_index')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


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
