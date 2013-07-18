from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("post.views",
    #url(r'^$', 'post.views.index', name='post_home'),
    url(r'^(?P<post_id>\d+)/$', 'detail', 
    	name='post_detail'),
    url(r'^create-post/$', 'create_post', 
    	name='create_post'),
    url(r'^edit-post/(?P<post_id>\d+)/$', 'edit_post', 
    	name='edit_post'),
)