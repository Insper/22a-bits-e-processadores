#!/usr/bin/env python3

from myhdl import *

# TODO
# - FlipFlopD.vhd
# - BinaryDigit.vhd
# - registerN
# - PC
#
#
# - PC.vhd
# - Ram4K.vhd
# - Ram512.vhd
# - Ram64.vhd
# - Ram8.vhd
# - TopLevel.vhd


@block
def ram(dout, din, addr, we, clk, width=16, depth=128):

    mem = [Signal(intbv(0)[width:]) for i in range(depth)]

    @always(clk.posedge)
    def logic():
        if we:
            mem[int(addr)].next = din
        dout.next = mem[int(addr)]

    return logic


@block
def pc(increment, load, i, output, rst, clk):
    @always_seq(clk.posedge, reset=rst)
    def logic():
        if load == 1:
            output.next = i
        elif increment == 1:
            output.next = output + 1
        else:
            output.next = output

    return logic


def register(i, load, output, clk):
    @always(clk.posedge)
    def logic():
        if load:
            output.next = i
        else:
            output.next = output

    return logic


def binaryDigit(i, load, output, clk):
    q, d, clear, presset = [Signal(bool(0)) for i in range(4)]
    dff_1 = dff(q, d, clear, presset, clk)

    @always_comb
    def comb():
        if load:
            d.next = i
        else:
            d.next = q
        output.next = q

    return instances()


def dff(q, d, clear, presset, clk):
    @always(clk.posedge)
    def logic():
        if clear:
            q.next = 0
        elif presset:
            q.next = 1
        else:
            q.next = d

    return logic
