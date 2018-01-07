from django.shortcuts import render
from  app.bopm2bsmengine import BopmData, JSONResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

def home(request):
    bopm = parse(request)
    bopmdata_json = json.dumps(bopm.as_json(), cls=DjangoJSONEncoder)
    return render(request, 'home.html', {"bopmdata": bopm,"bopmdata_json":bopmdata_json})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    return JSONResponse(parse(request).as_json())

def parse(request):
    stock_price = float(request.GET.get('stock',50))
    strick_price = float(request.GET.get('strike',50))
    rate = float(request.GET.get('rate',0.1))
    maturity = float(request.GET.get('maturity',1))
    volatility = float(request.GET.get('volatility',0.3))
    step = int(request.GET.get('step',50))
    return BopmData(stock_price, strick_price, rate, volatility,maturity, step)
