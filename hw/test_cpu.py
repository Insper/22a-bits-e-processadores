#!/usr/bin/env python3

from os import path, listdir
from myhdl import *
from cpu import *
from sequencial import *
from simulation import *


@block
def test_cpu():
    lst_data = []
    instruction = Signal(intbv(0))
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = ResetSignal(0, active=1, isasync=True)

    cpu_1 = cpu(
        inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, lst_data
    )

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    #    @instance
    #    def tb():
    #
    #        breakpoint()
    #        instruction.next = 0b000000000000000001  # leaw $1, %A
    #        yield delay(10)
    #        inMem.next = 13
    #        instruction.next = 0b100011100000010000  # movw (%A), %D
    #        yield delay(10)
    #        instruction.next = 0b000000000000000000  # leaw $0, %A
    #        yield delay(10)
    #        inMem.next = 15
    #        instruction.next = 0b100010000100010000  # addw (%A), %D, %D
    #        yield delay(10)
    #        instruction.next = 0b000000000000000010  # leaw $2, %A
    #        yield delay(10)
    #        instruction.next = 0b100000011000100000  # movw %D, (%A)
    #        yield delay(10)
    #        print(writeM)
    #        print(addressM)
    #        print(pcount)

    @instance
    def rst():
        rst.next = 1
        yield delay(5)
        rst.next = 0

    return instances()


def test_all():
    print("---- cpu ----")
    tb = traceSignals(test_cpu)
    sim = Simulation(tb)
    sim.run(2000)
    sim.quit()


if __name__ == "__main__":
    test_all()
