#!/usr/bin/env python3

from myhdl import *
from sequencial import *
import random

random.seed(5)
randrange = random.randrange


def convert_ram(hdl):
    din, dout = [Signal(intbv(0)[32:]) for i in range(2)]
    addr = Signal(intbv(0)[16:0])
    we, clk = [Signal(bool(0)) for i in range(2)]
    ram_1 = ram(dout, din, addr, we, clk, width=32, depth=256)
    ram_1.convert(hdl=hdl)


@block
def test_ram():
    din, dout, addr = [Signal(intbv(0)) for i in range(3)]
    we, clk = [Signal(bool(0)) for i in range(2)]
    ram_1 = ram(dout, din, addr, we, clk, width=32, depth=128)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        for i in range(10):
            din.next = din + 1
            addr.next = addr + 1
            we.next = 1
            yield clk.negedge
        we.next = 0
        addr.next = 0
        yield delay(20)
        for i in range(10):
            addr.next = addr + 1
            yield clk.negedge

    return ram_1, clkgen, stimulus


def test_pc():

    i, output = [Signal(intbv(0)) for i in range(2)]
    inc, load, clk = [Signal(bool(0)) for i in range(3)]
    rst = ResetSignal(0, active=0, isasync=True)
    pc_0 = pc(inc, load, i, output, rst, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def tb():
        rst.next = 1
        inc.next = 1
        yield delay(30)
        rst.next = 0
        for n in range(10):
            yield clk.negedge
        inc.next = 0
        for n in range(5):
            yield clk.negedge
        i.next = 32
        load.next = 1
        yield clk.negedge
        load.next = 0
        inc.next = 1

    return pc_0, tb, clkgen


def test_register():

    i, output = [Signal(intbv(0)) for i in range(2)]
    load, clk = [Signal(bool(0)) for i in range(2)]
    register_0 = register(i, load, output, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def tb():
        for n in range(10):
            yield clk.negedge
            i.next = randrange(2**16 - 1)
            load.next = 1
            yield clk.negedge
            i.next = 0
            load.next = 0

    return register_0, tb, clkgen


def test_binaryDigit():
    i, load, output, clk = [Signal(bool(0)) for i in range(4)]
    binaryDigit_0 = binaryDigit(i, load, output, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def tb():
        if output != 0:
            print("erro 1")
        yield delay(30)
        i.next = 1
        load.next = 1
        yield delay(25)
        if output != 1:
            print("erro 2")
        load.next = 0
        yield delay(25)
        i.next = 0
        load.next = 1
        yield delay(20)
        if output != 0:
            print("erro 3")
        load.next = 0

    return binaryDigit_0, clkgen, tb


def test_dff():
    q, d, clear, presset, clk = [Signal(bool(0)) for i in range(5)]
    dff_inst = dff(q, d, clear, presset, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        d.next = not q

    @instance
    def cleargen():
        clear.next = 1
        yield delay(20)
        i = 0
        while i < 5:
            if q != 0:
                print("erro clear")
            yield delay(10)
            i = i + 1
        clear.next = 0

    return dff_inst, clkgen, stimulus, cleargen


def test_all():
    print("---- dff ----")
    tb = traceSignals(test_dff)
    sim = Simulation(tb)
    sim.run(2000)
    sim.quit()

    print("---- binaryDigit ----")
    tb = traceSignals(test_binaryDigit)
    sim = Simulation(tb)
    sim.run(200)
    sim.quit()

    print("---- register ----")
    tb = test_register()
    sim = Simulation(tb)
    sim.run(500)
    sim.quit()

    print("---- pc ----")
    tb = test_pc()
    sim = Simulation(tb)
    sim.run(500)
    sim.quit()

    print("---- ram ----")
    tb = test_ram()
    tb.run_sim(500)


if __name__ == "__main__":
    test_all()
