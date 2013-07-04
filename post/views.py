from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Blog Posts!")

@login_required
def create_post(request):
    return HttpResponse("Create Post!")

def edit_post(request, post_id):
    return HttpResponse("Edit Post!")

def detail(request, post_id):
    return HttpResponse("Post Detail!")