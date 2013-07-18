from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("comment.views",
    #url(r'^$', 'comment.views.index', name="comment_home"),
    url(r'^add-comment/(?P<post_id>\d+)/$', 'add_comment', 
    	name="add_comment"),
    url(r'^add-reply/(?P<post_id>\d+)/$', 'add_reply', 
    	name="add_reply"),
    url(r'^approve-comment/(?P<activation_key>.+)/$', 'approve_comment', 
    	name='approve_comment'),
)