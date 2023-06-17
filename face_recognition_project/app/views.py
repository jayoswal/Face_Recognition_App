from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    print("[info] app - views - index")
    return HttpResponse("<h1> Hello World - Index</h1>")

def index1(request):
    print("[info] app - views - index1")
    return HttpResponse("<h1> Hello World - Index1</h1>")

def index2(request):
    print("[info] app - views - index2")
    return render(request, 'index.html')