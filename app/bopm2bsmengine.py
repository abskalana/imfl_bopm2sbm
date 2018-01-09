from math import exp
import math

class OptionStep():
    def __init__(self, step,bopm,bsm):
        self.step = step
        self.bopm = bopm
        self.bsm = bsm

    def as_json(self):
        return dict(
            step=self.step,
            bopm = self.bopm,
            bsm = self.bsm
        )
class BopmData():
    def __init__(self, stock_price, strike_price,rate,volatility,maturity,step, op_type = 0):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.rate = rate
        self.volatility = volatility
        self.maturity = maturity
        self.step = step
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
            op_type = self.op_type,
            optionsteps=[ob.as_json() for ob in self.optionsteps])

    def compute(self):
        rate = self.rate / 100.0
        volatility = self.volatility / 100.0
        self.bsm = black_schole(self.stock_price, self.strike_price, rate, volatility, self.maturity, self.op_type)
        for i in range(1, self.step+1):
            bopm = binomial(self.stock_price, self.strike_price, rate, volatility, self.maturity, i, self.op_type)
            self.optionsteps.append(OptionStep(i, bopm, self.bsm))
        self.bopm = bopm

def binomial(stock_price,strike_price,rate,volatility,maturity,step,op_type):
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
        if op_type == 1 :
            C[j] = max(strike_price - St[j], 0)
        else :
            C[j] = max(St[j] - strike_price, 0)

    for i in range(step, 0, -1):
        for j in range(0, i):
            C[j] = (1/a) * (p * C[j + 1] + (1-p) * C[j])

    return C[0]

def black_schole(stock_price,strike_price,rate,volatility,maturity,op_type):
    d1 = (math.log(stock_price/strike_price) + (rate +volatility*volatility/2)*maturity)/ (volatility* math.sqrt(maturity))
    d2 = d1 - volatility*math.sqrt(maturity)
    if op_type == 1:
        return strike_price * phi(-d2) - stock_price * phi(-d1)* math.exp(-rate * maturity)
    return stock_price * phi(d1) - strike_price * phi(d2) * math.exp(-rate * maturity)


def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0