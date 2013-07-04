from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from account.models import EmailChange

@login_required
def index(request):
    user = request.user
    profile = user.get_profile()
    email_change = EmailChange.objects.filter(user=request.user, is_active=True)[0] if EmailChange.objects.filter(user=request.user, is_active=True) else None
    return render(request, 'account/index.html', {'user': user, 'profile': profile, 'change': email_change})

#@user_passes_test(lambda u: u.is_anonymous())
def register_user(request):
    return HttpResponse("Register!")

#@user_passes_test(lambda u: u.is_anonymous(), reverse('account_home'))
def login_user(request):
    return HttpResponse("Login!")

#@login_required
def update_profile(request):
    return HttpResponse("Update Profile!")

#@login_required
def change_password(request):
    return HttpResponse("Change Password!")

#@login_required
def change_email(request):
    return HttpResponse("Change Email!")

#@login_required
def activate_email(request):
    return HttpResponse("Activate Email!")

#@login_required
def my_posts(request):
    return HttpResponse("My Posts!")

#@login_required
def logout_user(request):
    return HttpResponse("Logout!")
