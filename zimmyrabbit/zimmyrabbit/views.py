from django.shortcuts import render,redirect
from django.http import HttpResponse

def index(request) :
    return render(request, 'jenkins/main.html')


def check_model(request) :
    content = request.POST.get('content')
    scontent = sorted(set(content.split()))
    print(scontent)
    return redirect('zimmyrabbit:index')