from django.shortcuts import render
from  app.bopm2bsmengine import BopmData
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

def home(request):
    bopm = parse(request)
    bopm.compute()
    bopmdata_json = json.dumps(bopm.as_json(), cls=DjangoJSONEncoder)
    return render(request, 'home.html', {"bopmdata": bopm,"bopmdata_json":bopmdata_json})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    bopm = parse(request)
    bopm.compute()
    return JSONResponse(bopm.as_json())

def parse(request):
    stock_price = float(request.GET.get('stock',50))
    strick_price = float(request.GET.get('strike',50))
    rate = float(request.GET.get('rate',10))
    maturity = float(request.GET.get('maturity',1))
    volatility = float(request.GET.get('volatility',30))
    step = int(request.GET.get('step',50))
    fixed = bool(request.GET.get('fixed', False))
    return BopmData(stock_price, strick_price, rate, volatility,maturity, step,fixed)

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

