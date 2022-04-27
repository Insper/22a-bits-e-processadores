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


def ram_dump_file(mem, outFile):
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


mem = [Signal(intbv(0)) for i in range(2**15 - 1)]


@block
def ram_sim(dout, din, addr, we, clk, mifFile, width=16, depth=128, dump=True):
    ram_init_from_mif(mem, mifFile)

    @always(clk.posedge)
    def logic():
        if we:
            mem[addr.val].next = din
        dout.next = mem[addr.val]

    return instances()


# TODO: Edu consegue debugar isso e entender pq não funciona?
# com o dicionário, ele muda o valor do nada na execucao
# com dic seria bem melhor, pq conseuguimos exportar somente
# o que foi alterado, e ocupamos muito menos memória
@block
def ram_sim2(dout, din, addr, we, clk, mifFile, width=16, depth=128):
    memory = {}
    ram_init_from_mif(memory, mifFile)
    print("----init ")

    @always(clk.posedge)
    def access():
        if we:
            memory[int(addr.val)] = din.val
        else:
            if int(addr.val) in memory.keys():
                dout.next = memory[int(addr.val)]
            else:
                dout.next = 0

    return access


@block
def test_cpu(inRamMif, inRomHack):
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = Signal(bool(0))

    cpu_1 = cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk)
    ram_1 = ram_sim(
        inMem, outMem, addressM, writeM, clkMem, inRamMif, depth=2**15 - 1
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


if __name__ == "__main__":
    print("---- cpu ----")
    tb = test_cpu(
        "add_nasm/add0_in.mif",
        "add_nasm/add.hack",
    )
    tb.config_sim(trace=True, tracebackup=False)
    tb.run_sim(300)
    ram_dump_file(mem, "add_nasm/add.out")
    ram_test(mem, "add_nasm/add0_tst.mif")
