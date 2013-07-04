from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r'^$', 'post.views.index', name='post_home'),
    url(r'^(?P<post_id>\d+)/$', 'post.views.detail', name='post_detail'),
    url(r'^create-post/$', 'post.views.create_post', name='create_post'),
    url(r'^edit-post/(?P<post_id>\d+)/$', 'post.views.edit_post', name='edit_post'),
)