from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r'^$', 'comment.views.index', name="comment_home"),
    url(r'^add-comment/$', 'comment.views.add_comment', name="add_comment"),
)