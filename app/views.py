from django.shortcuts import render
from  app.bopm2bsmengine import BopmData, JSONResponse

def home(request):
    stock_price = float(request.GET.get('s', 50))
    strick_price = float(request.GET.get('k', 50))
    rate = float(request.GET.get('r', 5))
    maturity = float(request.GET.get('t', 1))
    volatility = float(request.GET.get('v', 0.3))
    step = float(request.GET.get('step', 2))
    bopm = BopmData(stock_price, strick_price, rate, maturity, volatility, step)
    return render(request, 'home.html', {"bopmdata": bopm})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    stock_price = float(request.GET.get('s', -1))
    strick_price = float(request.GET.get('k', -1))
    rate = float(request.GET.get('r', -1))
    maturity = float(request.GET.get('t', -1))
    volatility = float(request.GET.get('v', -1))
    step = float(request.GET.get('step', 0))
    bopm = BopmData(stock_price, strick_price, rate, maturity, volatility, step)
    return JSONResponse(bopm.as_json())