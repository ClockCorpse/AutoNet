from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'control/base.html')

def discover(request):
    return render(request,'control/discover.html')

def account_info(request):
    return render(request,'control/user_info.html')