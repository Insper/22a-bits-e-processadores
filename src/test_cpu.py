#!/usr/bin/env python3

from myhdl import *
from cpu import *
from sequencial import *

def rom_init_from_hack(fileName):
    with open(fileName) as f:
        return [int(l, 2) for l in f.read().splitlines()]


def ram_init_from_mif(mem, fileName):
    init = False
    with open(fileName) as f:
        for l in f.read().splitlines():
            if l.find("END") > -1:
                init = False
            if init:
                v = l.replace(";", ":").split(":")
                address = int(v[0])
                value = int(v[1], 2)
                mem[address] = Signal(value)
            if l.find("BEGIN") > -1:
                init = True


def ram_to_file(mem):
    with open("out.txt", "w") as f:
        for idx, x in enumerate(mem):
            f.write(str(idx) + " : " + bin(x, 16) + "\n")
        f.close()


@block
def rom_sim(dout, addr, clk, hackFile, width=16, depth=128):

    rom = rom_init_from_hack(hackFile)

    @always(clk.posedge)
    def access():
        address = int(addr)
        if address >= len(rom):
            dout.next = 0x20000
        else:
            dout.next = rom[address]

    return instances()


@block
def ram_sim(dout, din, addr, we, clk, mifFile, width=16, depth=128):

    mem = [Signal(intbv(0)) for i in range(depth)]
    ram_init_from_mif(mem, mifFile)

    f_write = Signal(bool(0))

    @always(clk.posedge)
    def logic():
        if we:
            mem[addr.val].next = din

            # schedule to dump to file on next clock
            f_write.next = True

        if f_write.val:
            # TODO: melhorar?
            ram_to_file(mem)
            f_write.next = False

        dout.next = mem[addr.val]

    return instances()


@block
def test_cpu():
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
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

    @always(delay(5))
    def clkgenMem():
        clkMem.next = not clkMem

    @instance
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
    tb.run_sim(70)
