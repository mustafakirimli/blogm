from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from account.models import UserProfile, EmailChange
from django.contrib import messages
from django.utils.translation import ugettext as _
from account.forms import RegisterForm, LoginForm, ProfileForm, UserForm, PasswordForm, EmailForm
import string, random

@login_required
def index(request):
    user = request.user
    profile = user.get_profile()
    email_change = EmailChange.pending_requests(user)
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

@user_passes_test(lambda u: u.is_anonymous(), login_url="/account/")
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, _("Invalid email/password"))
    else:
        form = LoginForm()
       
    return render(request, 'account/login.html', {
        'form': form,
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile informations updated succesfully."))
            return HttpResponseRedirect(reverse('update_profile'))
    else:
        form = ProfileForm(instance=request.user.get_profile())
       
    return render(request, 'account/profile.html', {
        'form': form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password informations updated succesfully."))
            return HttpResponseRedirect(reverse('change_password'))
    else:
        form = PasswordForm(instance=request.user)

    return render(request, 'account/password.html', {
        'form': form,
    })

#@login_required
def forgot_password(request):
    return HttpResponse("Forgot Password!")

@login_required
def change_email(request):
    email_change = EmailChange.pending_requests(request.user) if not request.GET.get("success") else None
    if request.method == 'POST':
        form = EmailForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()

            activation_key = ''.join([random.choice(string.digits + string.letters) for i in range(12)])
            EmailChange.objects.filter(user=request.user).update(is_active=False)
            emailChange = EmailChange.objects.create(user=request.user, email=request.POST.get("email"), is_active=True, activation_key=activation_key)
            emailChange.send_activation_email.delay(emailChange)
            messages.success(request, _("Email informations updated succesfully."))
            redirect_url = "%s%s" %(reverse('change_email'), "?success=true")
            return HttpResponseRedirect(redirect_url)
    else:
        form = EmailForm(instance=request.user)

    return render(request, 'account/email.html', {
        'form': form, 'change': email_change
    })

@login_required
def activate_email(request, activation_key):
    change = EmailChange.objects.get(user=request.user, is_active=True, activation_key=activation_key)
    request.user.email = change.email
    request.user.save()
    change.is_active = False
    change.save()
    messages.success(request, _("Email address activated"))
    return HttpResponseRedirect(reverse('account_home'))

#@login_required
def my_posts(request):
    return HttpResponse("My Posts!")

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
