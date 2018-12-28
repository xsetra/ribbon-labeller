from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import redirect

# Create your views here.


def change_password(request):
    payload = {}
    form = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            payload['success'] = "Password has been changed"
        else:
            payload['error'] = "Form isn't valid. Password hasn't been changed"
    else:
        form = PasswordChangeForm(request.user)
    payload['form'] = form
    return render(request, 'registration/change_password.html', context=payload)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pass)
            login(request, user)
            return redirect('data:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

