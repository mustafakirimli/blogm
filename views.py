from django.shortcuts import render
from django.core.cache import cache
from django.core.context_processors import csrf

from post.models import Post
from decorators import cache_on_auth


@cache_on_auth(600)
def home(request):
    """
    Homepage view getting latest 3 post and main post and rendering html
    """

    # get latest 3 posts from cache
    latest_posts = cache.get('latest_posts')

    # if cache is empty fetch from db
    if not latest_posts:
    	# fetch posts
    	latest_posts = Post.objects.latest_posts()[:3]

    	# cache latest posts
    	cache.set('latest_posts', latest_posts, 300)

    # get main post from cache
    main_post = cache.get('main_post')

    # if cache is empty fetch from db
    if not main_post:
        # fetch posts
        main_post = Post.objects.random_posts()[:1]

        # cache latest posts
        cache.set('main_post', main_post, 300)

    # return mainpage template
    return render(request, 'home.html', {
    	'latest_posts': latest_posts, 
    	'main_post': main_post
    })

@cache_on_auth(600)
def wrong(request):
    """
    This method testing for 500 error page
    """
    pass

def get_csrf(request):
    """
    Create csrf token and render in a html file
    """
    c = {}
    c.update(csrf(request))
    return render(request, 'csrf.html', c)