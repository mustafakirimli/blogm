from django.shortcuts import render
from post.models import Post

def home(request):
    latest_posts = Post.get_latest_post()
    #TODO: check count
    main_post = Post.get_main_post()[0] if Post.get_main_post() else None
    return render(request, 'home.html', {'latest_posts': latest_posts, 'main_post': main_post})

def wrong(request):
	pass