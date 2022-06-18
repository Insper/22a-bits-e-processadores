#!/usr/bin/env python3

from myhdl import *
from os import path, listdir
from tabulate import tabulate


def rom_init_from_hack(fileName):
    with open(fileName) as f:
        return [int(l, 2) for l in f.read().splitlines()]


def ram_init_from_mif(fileName, hasHead=True, sig=True):
    mem = {}
    init = not hasHead
    with open(fileName) as f:
        for l in f.read().splitlines():
            if not l:
                pass
            elif l.find("END") > -1:
                init = False
            elif l.find("BEGIN") > -1:
                init = True
            elif init:
                v = l.replace(";", ":").split(":")
                address = int(v[0])
                value = int(v[1], 2)
                if sig is True:
                    mem[address] = Signal(value)
                else:
                    mem[address] = value
    return mem


def mem_dump_file(mem, outFile):
    with open(outFile, "w") as f:
        for key in mem:
            f.write(str(key) + " : " + bin(mem[key].val, 16) + "\n")
        f.close()


def ram_test(ref, dump):
    cntErro = 0
    for key, value in ref.items():
        if key not in dump:
            dump[key] = 0
        if dump[key] != value:
            cntErro = cntErro + 1
            print("%s: %s | %s" % (key, bin(value, 16), bin(dump[key], 16)))
    return cntErro


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
def ram_sim(mem, dout, din, addr, we, clk, width=16, depth=128):
    @always(clk.posedge)
    def logic():
        if we:
            mem[int(addr.val)] = Signal(din.val)
        else:
            if int(addr.val) not in mem:
                dout.next = 0
            else:
                dout.next = mem[int(addr.val)]

    return instances()


def lstHeader():
    h = []
    h.append("ps")
    h.append("clock")
    h.append("instruction")
    h.append("pcout")
    h.append("s_regDout")
    h.append("s_regSout")
    h.append("s_regAout")
    h.append("c_muxALUI_A")
    h.append("c_muxSD_ALU")
    h.append("outM")
    h.append("writeM")
    h.append("inM")
    return h


def lstWrite(data, lstFile):
    f = open(lstFile, "w")
    f.write(tabulate(data, headers=lstHeader(), tablefmt="plain"))
    f.close()
