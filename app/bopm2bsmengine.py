import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from math import exp,sqrt


from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class BopmData():
    def __init__(self, stock_price, strike_price,rate,volatility,maturity,step):
        self.u = exp(volatility*sqrt(step))
        self.d = exp(-volatility * sqrt(step))

    def as_json(self):
        return dict(
            u=self.u,
            d=self.d)

def calculate_step(self, s, k,dt, u, d,r):
    p = (exp(r*dt)-d)/(u-d)
    fu = max(s*u -k,0)
    fd=  max(s*d-k,0)
    f = exp(-r*dt)*(fu*p+(1-p)*fd)
    return f



