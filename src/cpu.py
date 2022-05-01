#!/usr/bin/env python3

from myhdl import *
from ula import ula
from sequencial import pc


@block
def cpu(inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, lst_data):

    reg_d = Signal(intbv(0)[16:])
    reg_a = Signal(intbv(0)[16:])

    ula_x = Signal(intbv(0)[16:])
    ula_y = Signal(intbv(0)[16:])
    ula_out = Signal(intbv(0)[16:])
    ula_ctr = Signal(intbv(0)[6:])
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
        ula_ctr.next = instruction[13:7]
        if instruction[13] == 1:
            ula_y.next = inMem
        else:
            ula_y.next = reg_a

        ula_x.next = reg_d

        jmp = False
        if instruction[17] == 1 and instruction[3:0] > 0:
            if instruction[0] == 1:
                if ula_ng == 0 and ula_zr == 0:
                    jmp = True
            if instruction[1] == 1:
                if ula_zr == 1:
                    jmp = True
            if instruction[2] == 1:
                if ula_ng == 1:
                    jmp = True
            if instruction[3:0] == 0b111:
                jmp = True

        if jmp:
            pc_load.next = 1
        else:
            pc_load.next = 0

    @always(clk.posedge)
    def registers():
        if instruction[17] == False:
            reg_a.next = instruction[16:]
        else:
            if instruction[3] == 1:
                reg_a.next = ula_out
            else:
                reg_a.next = reg_a

            if instruction[4] == 1:
                reg_d.next = ula_out
            else:
                reg_d.next = reg_d

    @always(clk.posedge)
    def lst():
        muxALUIA = 0
        if instruction[17] == 1:
            muxALUIA = 1

        data = [
            0,
            bin(clk.val, 1),
            bin(instruction.val, 18),
            bin(pcount, 16),
            bin(reg_d, 16),
            bin(0, 16),
            bin(reg_a, 16),
            bin(muxALUIA, 1),
            bin(0, 1),
            bin(ula_out, 16),
            bin(writeM, 1),
            bin(inMem, 16),
        ]
        lst_data.append(data)

    return instances()
