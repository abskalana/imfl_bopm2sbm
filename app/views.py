import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response

def home(request):
    return render(request, 'home.html')

def documentation(request):
    return render(request, 'document.html')

def apropos(request):
    return render(request, 'about.html')

