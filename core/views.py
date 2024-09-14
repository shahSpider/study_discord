from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')


def room(request):
    return HttpResponse("Room page")