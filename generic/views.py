from django.shortcuts import render

# Create your views here.


def base(request):
    return render(request, 'index.html')


def homepage(request):
    return render(request, 'home.html')


def legal(request):
    return render(request, 'legal.html')
