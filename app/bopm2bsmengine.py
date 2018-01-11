from math import exp
import math

class OptionStep():
    def __init__(self, step,bopm,bsm):
        self.step = step
        self.bopm = bopm
        self.bsm = bsm
        self.diff = math.fabs(bopm - bsm)

    def as_json(self):
        return dict(
            step=self.step,
            diff = self.diff,
            bopm = self.bopm,
            bsm = self.bsm
        )
class BopmData():
    def __init__(self, stock_price, strike_price,rate,volatility,maturity,step_value,step_unit, op_type = 0,op_nat =0, ):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.rate = rate
        self.volatility = volatility
        self.maturity = maturity
        self.delta = 0
        self.u = 0
        self.d= 0
        self.diff = 0
        self.step_unit = step_unit
        self.step_value = step_value
        self.step = get_step(maturity,step_value,step_unit)
        self.op_nat = op_nat
        self.op_type = op_type
        self.optionsteps = []

    def as_json(self):
        return dict(
            stock_price = self.stock_price,
            strike = self.strike_price,
            rate=self.rate,
            volatility = self.volatility,
            maturity=self.maturity,
            step=self.step,
            u = self.u,
            d = self.d,
            op_nat = self.op_nat,
            diff = self.diff,
            deltat = self.delta,
            op_type = self.op_type,
            optionsteps=[ob.as_json() for ob in self.optionsteps])

    def compute(self):
        rate = self.rate / 100.0
        volatility = self.volatility / 100.0
        self.u = up(volatility,self.maturity,self.step)
        self.d = down(volatility, self.maturity, self.step)
        self.bsm = black_schole(self.stock_price, self.strike_price, rate, volatility, self.maturity, self.op_type,self.op_nat)
        self.delta = delta_bsm(self.stock_price, self.strike_price, rate, volatility, self.maturity, self.op_type,self.op_nat)
        for i in range(1, self.step+1):
            bopm = binomial(self.stock_price, self.strike_price, rate, volatility, self.maturity, i, self.op_type,self.op_nat)
            self.optionsteps.append(OptionStep(i, bopm, self.bsm))
        self.bopm = bopm
        self.diff = math.fabs(bopm - self.bsm)


def binomial(stock_price,strike_price,rate,volatility,maturity,step,op_type,op_nat = 0):
    dt = maturity / step
    u = up(volatility,maturity,step)
    d = down(volatility,maturity,step)
    a = exp(rate*dt)
    p = (a - d) / (u - d)

    St = [0] * (step + 1)
    C  = [0] * (step + 1)

    St[0] = stock_price * d ** step

    for j in range(1, step + 1):
        St[j] = St[j - 1] * u / d

    for j in range(1, step + 1):
        if op_type == 1 :
            C[j] = max(strike_price - St[j], 0)
        else :
            C[j] = max(St[j] - strike_price, 0)

    for i in range(step, 0, -1):
        for j in range(0, i):
            C[j] = (1/a) * (p * C[j + 1] + (1-p) * C[j])

    return C[0]

def black_schole(stock_price,strike_price,rate,volatility,maturity,op_type,op_nat = 0 ):
    d1 = (math.log(stock_price/strike_price) + (rate +volatility*volatility/2)*maturity)/ (volatility* math.sqrt(maturity))
    d2 = d1 - volatility*math.sqrt(maturity)
    if op_type == 1:
        return strike_price * phi(-d2) - stock_price * phi(-d1)* math.exp(-rate * maturity)
    return stock_price * phi(d1) - strike_price * phi(d2) * math.exp(-rate * maturity)

def delta_bsm(stock_price,strike_price,rate,volatility,maturity,op_type,op_nat = 0):
    d1 = (math.log(stock_price/strike_price) + (rate +volatility*volatility/2)*maturity)/ (volatility* math.sqrt(maturity))
    if op_type == 1:
        return phi(d1)-1
    return phi(d1);

def up(volatility,maturity,step):
    return  math.exp(volatility * math.sqrt(maturity / step))

def down(volatility,maturity,step):
    return  (1/up(volatility,maturity,step))

def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def get_step(maturity,step_value,step_unit):
    result = max(maturity / step_value, 1)

    if step_unit.startswith('w'):
        step_in_years = (step_value*7)/ 360.0
        result = max(maturity / step_in_years, 1)

    if step_unit.startswith('m'):
        step_in_years = step_value / 12.0
        result = max(maturity / step_in_years, 1)

    if step_unit.startswith('d'):
        step_in_years = step_value / 360.0
        result = max(maturity / step_in_years, 1)
    return math.ceil(result)