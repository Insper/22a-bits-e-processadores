#!/usr/bin/env python3

from myhdl import block, always_comb


@block
def and16(q, a, b):
    @always_comb
    def comb():
        q.next = a[:] & b[:]

    return comb


@block
def or8way(a, b, c, d, e, f, g, h, q):
    @always_comb
    def comb():
        q.next = a | b | c | d | e | f | g | h

    return comb


@block
def orNway(a, q):
    @always_comb
    def comb():
        t = 0
        for i in range(0, a.max):
            t = a[i] | t
        q.next = t

    return comb


@block
def barrelShifter(a, dir, size, q):
    @always_comb
    def comb():
        if dir:
            q.next = a << size
        else:
            q.next = a >> size

    return comb
