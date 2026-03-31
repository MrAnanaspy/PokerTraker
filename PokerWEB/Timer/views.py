from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def get_index(request):
    person ='ert'
    return render(request, "timer.html", context={'persons':person})