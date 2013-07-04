from django.http import HttpResponse

def index(request):
    return HttpResponse("Comment Index!")

def add_comment(request):
    return HttpResponse("Add Comment!")
