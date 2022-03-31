#!/usr/bin/env python3
from myhdl import block, always_comb

@block
def mux2Way(q, a, b, sel):

    @always_comb
    def comb():
        if (sel == 0):
            q.next = a
        else:
            q.next = b

    return comb

@block
def mux4Way(q, a, b, c, d, sel):

    @always_comb
    def comb():
        if (sel == 0):
            q.next = a
        elif (sel == 1):
            q.next = b
        elif (sel == 2):
            q.next = c
        else:
            q.next = d

    return comb

@block
def mux8Way(q, a, b, c, d, e, f, g, h, sel):

    @always_comb
    def comb():
        inMux = [a, b, c, d, e, f, g, h]
        q.next = inMux[sel]
    return comb


@block
def mux(q, signals, sel):
    @always_comb
    def comb():
        q.next = signals[sel]
    return comb
