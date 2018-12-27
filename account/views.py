from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
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
