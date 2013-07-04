from django.shortcuts import render
from post.models import Post

def home(request):
    post = Post()
    latest_posts = post.getLatestPost()
    #TODO: check count
    main_post = post.getMainPost()[0] if post.getMainPost() else None
    return render(request, 'home.html', {'latest_posts': latest_posts, 'main_post': main_post})