import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from math import exp,sqrt
import math


from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class OptionStep():
    def __init__(self, option, step):
        self.option = option
        self.step = step

    def as_json(self):
        return dict(
            option=self.option,
            step=self.step)


class BopmData():
    def __init__(self, stock_price, strike_price,rate,volatility,maturity,step):
        dt = maturity/step
        self.u = exp(volatility*sqrt(dt))
        self.d = exp(-volatility * sqrt(dt))
        self.stock = stock_price
        self.strike_price = strike_price
        self.rate = rate
        self.volatility = volatility
        self.maturity = maturity
        self.step = step
        self.optionsteps = []
        for i in range(1,step):
            price = calculate_step(stock_price,strike_price,rate,volatility,maturity,i,False)
            self.optionsteps.append(OptionStep(price,i))

    def as_json(self):
        return dict(
            u = self.u,
            d = self.d,
            stock = self.stock,
            strike = self.strike_price,
            volatility = self.volatility,
            rate= self.rate,
            maturity = self.maturity,
            step = self.step,
            optionsteps=[ob.as_json() for ob in self.optionsteps])

def calculate_step(stock_price,strike_price,rate,volatility,maturity,step,put):
    dt = maturity / step
    u = math.exp(volatility * math.sqrt(dt))
    d = math.exp(-volatility * math.sqrt(dt))
    a = exp(rate*dt)
    p = (a - d) / (u - d)

    St = [0] * (step + 1)
    C  = [0] * (step + 1)

    St[0] = stock_price * d ** step

    for j in range(1, step + 1):
        St[j] = St[j - 1] * u / d

    for j in range(1, step + 1):
        if put :
            C[j] = max(strike_price - St[j], 0)
        else :
            C[j] = max(St[j] - strike_price, 0)

    for i in range(step, 0, -1):
        for j in range(0, i):
            C[j] = (1/a) * (p * C[j + 1] + (1-p) * C[j])

    return C[0]
