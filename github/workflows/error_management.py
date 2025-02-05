import numpy as np
import scipy as scp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
from math import floor
from statistics import mean, stdev

class Number():
    def __init__(self, value, error):
        self.value = value
        self.error = error
    
    def __str__(self):
        return f"{self.value} +- {self.error}"
    
    def __mul__(self, other):
        return Number(other*self.value, other*self.error)
    
    def __rmul__(self, other):
        return Number(other*self.value, other*self.error)
    
    def normalize(self):
        X = self.value
        dX = self.error

        return Number(round_order(X, order(dX)), round_order(dX, order(dX)))

    def mult(self, y):    
        X = self.value
        dX = self.error
        Y = y.value
        dY = y.error
        error = abs(X*dY)+abs(Y*dX)
        error = round_order(error, order(error))
        value = round_order(X*Y, order(error))
        return Number(value, error)

    def divide(self, y):
        X = self.value
        dX = self.error
        Y = y.value
        dY = y.error
        error = abs(dX/Y)+abs(X/(Y**2)*dY)
        error = round_order(error, order(error))
        value = round_order(X/Y, order(error))
        return Number(value, error)

    def plus(self, y):
        X = self.value
        dX = self.error
        Y = y.value
        dY = y.error
        error = abs(dX)+abs(dY)
        error = round_order(error, order(error))
        value = round_order(X+Y, order(error))
        return Number(value, error)

    def minus(self, y):
        X = self.value
        dX = self.error
        Y = y.value
        dY = y.error
        error = abs(dX)+abs(dY)
        error = round_order(error, order(error))
        value = round_order(X-Y, order(error))
        return Number(value, error)

    def sqroot(self):
        X = self.value
        dX = self.error
        error = abs(dX/np.sqrt(X))/2
        error = round_order(error, order(error))
        value = round_order(np.sqrt(X), order(error))
        return Number(value, error)
    
    def pow(self, n):
        X = self.value
        dX = self.error

        error = n*X**(n-1)*dX
        error = round_order(error, order(error))

        value = X**n
        value = round_order(value, order(error))

        return Number(value, error)


def order(x):
    return int((-floor(np.log10(x))))

def round_order(x, order):
    return round(x, order)

def adjust_to_line(x, y):

    def line(x, a, b):
        return a*x+b
    popt, pcov = curve_fit(line, x, y)
    for i in range(len(popt)):
        a = popt[i]
        da = np.sqrt(np.diag(pcov))[i]
        _order = order(da)
        a = round_order(a, _order)
        da = round_order(da, _order)
        print(f"{a} +- {da}", end='\n')


def mult(x: Number, y: Number):    
    X = x.value
    dX = x.error
    Y = y.value
    dY = y.error
    error = abs(X*dY)+abs(Y*dX)
    error = round_order(error, order(error))
    value = round_order(X*Y, order(error))
    return Number(value, error)

def divide(x: Number, y: Number):
    X = x.value
    dX = x.error
    Y = y.value
    dY = y.error
    error = abs(dX/Y)+abs(X/(Y**2)*dY)
    error = round_order(error, order(error))
    value = round_order(X/Y, order(error))
    return Number(value, error)

def summation(x: Number, y: Number):
    X = x.value
    dX = x.error
    Y = y.value
    dY = y.error
    error = abs(dX)+abs(dY)
    error = round_order(error, order(error))
    value = round_order(X+Y, order(error))
    return Number(value, error)

def sqroot(x: Number):
    X = x.value
    dX = x.error
    error = abs(dX/np.sqrt(X))/2
    error = round_order(error, order(error))
    value = round_order(np.sqrt(X), order(error))
    return Number(value, error)