from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r'^$', 'account.views.index', name='account_home'),
    url(r'^index/$', 'account.views.index', name='account_home_index'),
    url(r'^register/$', 'account.views.register_user', name='register'),
    url(r'^login/$', 'account.views.login_user', name='login'),
    url(r'^update-profile/$', 'account.views.update_profile', name='update_profile'),
    url(r'^change-password/$', 'account.views.change_password', name='change_password'),
    url(r'^change-email/$', 'account.views.change_email', name='change_email'),
    url(r'^activate-email/$', 'account.views.activate_email', name='activate_email'),
    url(r'^my-posts/$', 'account.views.my_posts', name='my_posts'),
    url(r'^logout/$', 'account.views.logout_user', name='logout')
)