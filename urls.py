from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blogm.views.home', name='home'),
    # url(r'^blogm/', include('blogm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # django filatpages
    url(r'^pages/', include('django.contrib.flatpages.urls'), name='pages'),

    # post app
    url(r'^post/', include('blogm.post.urls')),

    # comment app
    url(r'^comment/', include('blogm.comment.urls')),

    # account app
    url(r'^account/', include('blogm.account.urls')),

    url(r'^wrong/', 'blogm.views.wrong', name='wrong'),

    # media requests
    url(r'^media/(?P<path>.*)$',
         "django.views.static.serve",
         dict(document_root = settings.MEDIA_ROOT, show_indexes = True)),
)
