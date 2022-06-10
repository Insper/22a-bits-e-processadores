#!/usr/bin/env python3

from myhdl import *
from cpu import *
from sequencial import *


def z01_convert():
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = ResetSignal(1, active=0)
    cpu_1 = cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, "")
    cpu_1.convert(hdl="VHDL")


z01_convert()
