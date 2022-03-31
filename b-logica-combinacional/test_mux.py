#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from mux import mux, mux8Way, mux4Way, mux2Way

random.seed(5)
randrange = random.randrange


def convert_mux2Way(hdl):
    q, a, b = [Signal(intbv(0)[8:0]) for i in range(3)]
    sel = Signal(bool(0))

    mux2Way_1 = mux2Way(q, a, b, sel)
    mux2Way_1.convert(hdl=hdl)


@block
def test_mux2Way():
    q, a, b = [Signal(intbv(0)) for i in range(3)]
    muxIn = [a, b]
    sel = Signal(bool(0))
    mux2Way_1 = mux2Way(q, a, b, sel)

    @instance
    def stimulus():
        erro_cnt = 0
        a.next, b.next = [randrange(8) for i in range(2)]
        print("q    a    b    sel ")

        for i in range(2):
            sel.next = i
            yield delay(10)
            if q != muxIn[i]:
                print("Erro:", end="")
                erro_cnt = erro_cnt + 1
            print("%s %s %s %s" % (bin(q, 4), bin(a, 4), bin(b, 4), bin(sel, 2)))
        print("Erros: %d" % erro_cnt)

    return mux2Way_1, stimulus


@block
def test_mux4Way():
    q, a, b, c, d = [Signal(intbv(0)) for i in range(5)]
    muxIn = [a, b, c, d]
    sel = Signal(intbv(0))
    mux4Way_1 = mux4Way(q, a, b, c, d, sel)

    @instance
    def stimulus():
        erro_cnt = 0
        a.next, b.next, c.next, d.next = [randrange(8) for i in range(4)]

        print("q    a    b    c    d    sel ")
        for i in range(4):
            sel.next = i
            yield delay(10)
            import pdb

            pdb.set_trace()
            if q != muxIn[i]:
                print("Erro:", end="")
                erro_cnt = erro_cnt + 1
            print(
                "%s %s %s %s %s %s"
                % (bin(q, 4), bin(a, 4), bin(b, 4), bin(c, 4), bin(d, 4), bin(sel, 2))
            )
        print("Erros: %d" % erro_cnt)

    return mux4Way_1, stimulus


@block
def test_mux8Way():
    q, a, b, c, d, e, f, g, h = [Signal(intbv(0)) for i in range(9)]
    muxIn = [a, b, c, d, e, f, g, h]
    sel = Signal(intbv(0))
    mux8Way_1 = mux8Way(q, a, b, c, d, e, f, g, h, sel)

    @instance
    def stimulus():
        erro_cnt = 0
        a.next, b.next, c.next, d.next = [randrange(8) for i in range(4)]
        e.next, f.next, g.next, h.next = [randrange(8) for i in range(4)]

        for i in range(4):
            sel.next = i
            yield delay(10)
            if q != muxIn[i]:
                print("Erro:", end="")
                erro_cnt = erro_cnt + 1
        print("Erros: %d" % erro_cnt)

    return mux8Way_1, stimulus


if __name__ == "__main__":
    print("---- mux2Way ----")
    tb = test_mux2Way()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- mux4Way ----")
    tb = test_mux4Way()
    tb.run_sim()

    print("---- mux8Way ----")
    tb = test_mux8Way()
    tb.run_sim()

    print("---- muxGeneric ----")
    tb = test_mux()
    tb.run_sim()
