#!/usr/bin/env python3

from myhdl import *
from os import path, listdir


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


def mem_dump_file(mem, outFile):

    with open(outFile, "w") as f:
        for idx, x in enumerate(mem):
            f.write(str(idx) + " : " + bin(x, 16) + "\n")
        f.close()


def ram_test(mem, testFile):
    cntErro = 0
    with open(testFile, "r") as f:
        for l in f.read().splitlines():
            if len(l.strip()):
                addrBin, valueBin = l.split(":")
                addr = int(addrBin)
                value = int(valueBin, 2)
                valueMem = int(mem[int(addr)])
                if valueMem != value:
                    cntErro = cntErro + 1
                    print("%s: %s | %s" % (addr, bin(value, 16), bin(valueMem, 16)))
        return cntErro
    return -1


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


def ram_clear(mem, depth):
    mem = [Signal(intbv(0)) for i in mem]


@block
def ram_sim(mem, dout, din, addr, we, clk, mifFile, width=16, depth=128):
    ram_init_from_mif(mem, mifFile)

    @always(clk.posedge)
    def logic():
        if we:
            mem[addr.val].next = din
        dout.next = mem[addr.val]

    return instances()
