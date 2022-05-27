#!/usr/bin/env python3

from myhdl import *
from cpu import *
from sequencial import *
from simulation import *


def z01_convert():
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = ResetSignal(1, active=0)
    cpu_1 = cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, "")
    cpu_1.convert(hdl="VHDL")


@block
def z01_sim(mem, inRamMif, inRomHack, lst_data):
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = ResetSignal(0, active=1, isasync=True)

    cpu_1 = cpu(
        inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, lst_data
    )
    ram_1 = ram_sim(
        mem, inMem, outMem, addressM, writeM, clkMem, inRamMif, depth=2**15 - 1
    )
    rom_1 = rom_sim(instruction, pcount, clk, inRomHack)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(delay(5))
    def clkgenMem():
        clkMem.next = not clkMem

    @instance
    def rst():
        rst.next = 1
        yield delay(5)
        rst.next = 0

    return instances()
