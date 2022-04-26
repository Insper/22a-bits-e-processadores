#!/usr/bin/env python3

from myhdl import *
from cpu import *
from sequencial import *


@block
def test_cpu():
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    rst = Signal(bool(0))

    cpu_1 = cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk)
    ram_1 = ram_sim(
        inMem,
        outMem,
        addressM,
        writeM,
        clk,
        "add_nasm/add0_in.mif",
        depth=2**15 - 1,
    )
    rom_1 = rom_sim(instruction, pcount, clk, "add_nasm/add.hack")

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always_comb
    def rst():
        rst.next = 1
        yield delay(5)
        rst.next = 0
        yield delay(500)

    # def clkgen():
    #    @instance
    #    def stimulus():
    #        # leaw %a, 1
    #        instruction.next = 0b000000000000001000
    #        yield clk.posedge
    #
    #        # movw %A, %D
    #        instruction.next = 0b100001100000010000
    #        yield clk.posedge
    #
    #        # incw %D
    #        instruction.next = 0b100000111110010000
    #        yield clk.posedge
    #
    #        # jump gt
    #        instruction.next = 0b100000011000000001
    #        yield clk.posedge
    #
    #        # nop
    #        instruction.next = 0b100001100000000000
    #        yield clk.posedge

    return instances()


if __name__ == "__main__":
    print("---- cpu ----")
    tb = test_cpu()
    tb.config_sim(trace=True, tracebackup=False)
    tb.run_sim(500)
