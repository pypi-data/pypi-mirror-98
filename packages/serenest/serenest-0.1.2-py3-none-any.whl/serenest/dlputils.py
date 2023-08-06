#!/usr/bin/env python3

from math import ceil, sqrt
from serenest.cryptoutils import modinverse, is_prime

def bsgs(generator, element, p):
    """
    Shanks' babystep-giantstep algorithm
    based on https://en.wikipedia.org/wiki/Baby-step_giant-step
    """
    if not(is_prime(p)):
        return str(p) + " is not a prime"
    
    #since p is prime, order = p-1
    order = p-1
    m = ceil(sqrt(order))
    babysteps = {pow(generator, i, p): i for i in range(m)}
    
    #giant steps
    intermediary = pow(modinverse(generator, p), m, p)
    gamma = element
    
    for i in range(m):
        if gamma in babysteps.keys():
            return i*m + babysteps[gamma]
        gamma = (gamma * intermediary)%p
    return "Are you sure " + str(generator) + " is a generator for " + str(p) + "?"

