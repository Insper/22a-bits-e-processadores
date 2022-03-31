#!/usr/bin/env python3
from myhdl import block, always_comb, Signal, intbv


@block
def deMux2Way(a, q0, q1, sel):
    @always_comb
    def comb():
        if sel == 0:
            q0.next = a
            q1.next = 0
        else:
            q0.next = 0
            q1.next = a

    return comb


@block
def deMux4Way(a, q0, q1, q2, q3, sel):
    @always_comb
    def comb():
        q0.next = 0
        q1.next = 0
        q2.next = 0
        q3.next = 0

        if sel == 0:
            q0.next = a
        elif sel == 1:
            q1.next = a
        elif sel == 2:
            q2.next = a
        else:
            q3.next = a

    return comb


@block
def deMux8Way(a, q0, q1, q2, q3, q4, q5, q6, q7, sel):
    @always_comb
    def comb():
        q0.next = 0
        q1.next = 0
        q2.next = 0
        q3.next = 0
        q4.next = 0
        q5.next = 0
        q6.next = 0
        q7.next = 0

        if sel == 0:
            q0.next = a
        elif sel == 1:
            q1.next = a
        elif sel == 2:
            q2.next = a
        elif sel == 3:
            q3.next = a
        elif sel == 4:
            q4.next = a
        elif sel == 5:
            q5.next = a
        elif sel == 6:
            q6.next = a
        else:
            q7.next = a

    return comb
