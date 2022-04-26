#!/usr/bin/env python3

from myhdl import *
from ula import *
from sequencial import pc


@block
def cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk):

    reg_d = Signal(intbv(2)[16:])
    reg_a = Signal(intbv(2)[16:])

    ula_x = Signal(intbv(1)[16:])
    ula_y = Signal(intbv(2)[16:])
    ula_out = Signal(intbv(0)[16:])
    ula_ctr = Signal(intbv(0))
    ula_zr = Signal(bool(0))
    ula_ng = Signal(bool(0))

    pc_load = Signal(bool(0))

    ula_1 = ula(ula_x, ula_y, ula_ctr, ula_zr, ula_ng, ula_out)
    pc_1 = pc(1, pc_load, reg_a, pcount, rst, clk)

    @always_comb
    def memory_access():
        writeM.next = instruction[5]
        addressM.next = reg_a
        outMem.next = ula_out

    @always_comb
    def controlUnit():
        ula_ctr.next = instruction[12:7]
        if instruction[13] == 1:
            ula_y.next = inMem
        else:
            ula_y.next = reg_a

        ula_x.next = reg_d

        jmp = 0
        if instruction[17] == 1 and instruction[3:0] > 0:
            if instruction[0] == 1:
                if ula_ng == 0 and ula_zr == 0:
                    jmp = jmp + 1
            if instruction[1] == 1:
                if ula_ng == 0 and ula_zr == 1:
                    jmp = jmp + 1
            if instruction[2] == 1:
                if ula_ng == 1 and ula_zr == 0:
                    jmp = jmp + 1

        if jmp != 0:
            pc_load.next = 1
        else:
            pc_load.next = 0

    @always(clk.posedge, rst.posedge)
    def registers():
        if rst:
            reg_a.next = 0
            reg_d.next = 0
        elif clk:
            if instruction[17] == False:
                reg_a.next = instruction[16:]
            else:
                #                print(
                #                    "%s %s %s" % (bin(instruction, 16), bin(reg_a, 16), bin(reg_d, 16))
                #                )

                if instruction[3] == 1:
                    reg_a.next = ula_out
                else:
                    reg_a.next = reg_a

                if instruction[4] == 1:
                    reg_d.next = ula_out
                    print(bin(ula_out, 16))
                    print(bin(instruction))
                else:
                    reg_d.next = reg_d

    return instances()


