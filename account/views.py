import string
import random
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.utils.translation import ugettext as _
from django.contrib import messages


from post.models import Post
from account.models import UserProfile, EmailChange
from account.forms import (RegisterForm, LoginForm, ProfileForm, 
                           UserForm, PasswordForm, EmailForm)

@login_required
def index(request):
    # get user
    user = request.user
    
    # get profile
    profile = user.get_profile()

    # get email change requests for user
    email_change = EmailChange.pending_requests(user)
    
    return render(request, 'account/index.html', {
        'user': user, 
        'profile': profile, 
        'change': email_change
    })

@user_passes_test(lambda u: u.is_anonymous())
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form, it gets user object
            user = form.save()
            
            # get user profile
            profile = user.get_profile()

            # send activation email to user
            profile.send_activation_email.delay(profile)
            
            messages.info(request, _("Thanks for registering. Please check "
                                     "your inbox for activation email."))

            # Redirect to account home page
            return redirect("home") 
    else:
        form = RegisterForm()
       
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

    return redirect("account_home")

@user_passes_test(lambda u: u.is_anonymous(), login_url="/account/")
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
       
    return render(request, 'account/login.html', {
        'form': form,
    })

@login_required
def update_profile(request):
    # get user profile
    profile = request.user.get_profile()

    if request.method == 'POST':
        form = ProfileForm(request.POST, 
                           request.FILES, 
                           instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated succesfully."))
            return redirect('update_profile')
    else:
        form = ProfileForm(instance=profile)
       
    return render(request, 'account/profile.html', {
        'form': form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST,
                            instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password  updated succesfully."))
            return redirect('change_password')
    else:
        form = PasswordForm(instance=request.user)

    return render(request, 'account/password.html', {
        'form': form,
    })

#@login_required
#TODO: not implemented
def forgot_password(request):
    return HttpResponse("Forgot Password!")

@login_required
def change_email(request):
    # pending email change requests
    email_change = EmailChange.pending_requests(request.user)

    # dont show email change request if requests created now
    if request.GET.get("success"):
        email_change = False

    if request.method == 'POST':
        form = EmailForm(request.POST,
                         instance=request.user)
        
        # new email address
        email = request.POST.get("email")

        if form.is_valid():
            form.save()

            # create email change requests
            email_change = EmailChange.create_request(request.user, email)

            # send email activation mail
            email_change.send_activation_email.delay(email_change)

            messages.success(request, _('Email change request created. '
                                        'Please check your email box'))

            # redirect to same page with success parameters
            response = redirect("change_email")
            response['Location'] += '?success=true'
            return response
    else:
        # create email change request form
        form = EmailForm(instance=request.user)

    return render(request, 'account/email.html', {
        'form': form, 
        'change': email_change
    })

@login_required
def activate_email(request, activation_key):
    ec = get_object_or_404(EmailChange,
                           activation_key=activation_key)

    # process email change request
    ec.activate_email()

    # add success message
    messages.success(request, _("Your email address activated"))

    # redirect to homepage
    return redirect('home')

@login_required
def my_posts(request):
    """
    Return users all post
    """
    posts = Post.objects.filter(user=request.user)
    return render(request, 'account/posts.html', {
        'posts': posts
    })

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')
