from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from account.models import UserProfile, EmailChange 
from django.contrib import messages
from django.utils.translation import ugettext as _
from account.forms import RegisterForm

@login_required
def index(request):
    user = request.user
    profile = user.get_profile()
    email_change = EmailChange.objects.filter(user=request.user, is_active=True)[0] if EmailChange.objects.filter(user=request.user, is_active=True) else None
    return render(request, 'account/index.html', {'user': user, 'profile': profile, 'change': email_change})

@user_passes_test(lambda u: u.is_anonymous())
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, _("Thanks for registering. Please check your email box for activation."))
            profile = new_user.get_profile()
            profile.send_activation_email.delay(profile)
            return HttpResponseRedirect(reverse("account_home")) # Redirect after POST
    else:
        form = RegisterForm() # An unbound form
       
    return render(request, 'account/register.html', {
        'form': form,
    })

def activate_account(request, activation_key):
    try:
        # get user profile with given activation key
        p = get_object_or_404(UserProfile, activation_key=activation_key)
        # activate user
        p.activate()
        # redirect to account index page and add success message
        messages.info(request, _("Account activated."))
    except:
        messages.info(request, _("Account activation problem!"))

    return HttpResponseRedirect(reverse("account_home"))

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
