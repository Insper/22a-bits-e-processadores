#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from ports import *

random.seed(5)
randrange = random.randrange


@block
def test_and16():

    # q, a, b = [Signal(intbv(0)) for i in range(3)]
    q = Signal(intbv(0))
    a = Signal(intbv(0))
    b = Signal(intbv(0))

    and16_1 = and16(q, a, b)

    @instance
    def stimulus():
        print("q a b")
        a.next, b.next = 1, 2
        q.next
        yield delay(10)
        print("%s %s %s" % (bin(q, 4), bin(a, 4), bin(b, 4)))

    return and16_1, stimulus


@block
def test_orNway():
    q = Signal(bool(0))
    i = Signal(intbv(2, max=8))
    orNway_1 = orNway(i, q)

    @instance
    def stimulus():
        erro_cnt = 0
        for x in range(0, 32):
            i.next = randrange(8)
            yield delay(10)
            if i.next > 0:
                if q < 0:
                    erro_cnt = erro_cnt + 1
                    print("Erro:", end="")
            else:
                if q > 0:
                    erro_cnt = erro_cnt + 1
                    print("Erro:", end="")

            if erro_cnt:
                print("%s %s" % (bin(i, i.max), q))

    return orNway_1, stimulus


@block
def test_barrelShifter():
    q = Signal(intbv(0))
    a = Signal(intbv(8))
    dir = Signal(bool(1))
    barrelShifter_1 = barrelShifter(a, dir, 2, q)

    @instance
    def stimulus():
        yield delay(10)
        print(bin(q, 8))

    return barrelShifter_1, stimulus


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


@block
def test_deMux4Way():
    a, q0, q1, q2, q3 = [Signal(intbv(0)) for i in range(5)]
    sel = Signal(intbv(0))
    deMuxOuts = [q0, q1, q2, q3]
    deMux4Way_1 = deMux4Way(a, q0, q1, q2, q3, sel)

    @instance
    def stimulus():
        erroCnt = 0
        a.next = randrange(4)
        for i in range(4):
            sel.next = i
            yield delay(10)
            if deMuxOuts[i] != a:
                print("Erro: sel:%s a:%s q:%s" % (sel, a, deMuxOuts))
                erroCnt = erroCnt + 1
        print("Erros: %d" % erroCnt)

    return deMux4Way_1, stimulus


@block
def test_deMux8Way():
    a, q0, q1, q2, q3, q4, q5, q6, q7 = [Signal(intbv(0)) for i in range(9)]
    sel = Signal(intbv(0))
    deMuxOuts = [q0, q1, q2, q3, q4, q5, q6, q7]
    deMux8Way_1 = deMux8Way(a, q0, q1, q2, q3, q4, q5, q6, q7, sel)

    @instance
    def stimulus():
        erroCnt = 0
        a.next = randrange(8)
        for i in range(8):
            sel.next = i
            yield delay(10)
            if deMuxOuts[i] != a:
                print("Erro: sel:%s a:%s q:%s" % (sel, a, deMuxOuts))
                erroCnt = erroCnt + 1
        print("Erros: %d" % erroCnt)

    return deMux8Way_1, stimulus


@block
def test_deMux2Way():
    a, q0, q1 = [Signal(intbv(0)) for i in range(3)]
    sel = Signal(intbv(0))
    deMuxOuts = [q0, q1]
    deMux2Way_1 = deMux2Way(a, q0, q1, sel)

    @instance
    def stimulus():
        erroCnt = 0
        a.next = randrange(4)
        for i in range(2):
            sel.next = i
            yield delay(10)
            if deMuxOuts[i] != a:
                print("Erro: sel:%s a:%s q:%s" % (sel, a, deMuxOuts))
                erroCnt = erroCnt + 1
        print("Erros: %d" % erroCnt)

    return deMux2Way_1, stimulus


def test_all():
    print("---- and16 ----")
    tb = test_and16()
    tb.run_sim()

    print("---- or8way ----")
    tb = test_orNway()
    tb.run_sim()

    print("---- barrelshifter ----")
    tb = test_barrelShifter()
    tb.run_sim()

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

    print("---- deMux2Way ----")
    tb = test_deMux2Way()
    tb.run_sim()

    print("---- deMux4Way ----")
    tb = test_deMux4Way()
    tb.run_sim()

    print("---- deMux8Way ----")
    tb = test_deMux8Way()
    tb.run_sim()


if __name__ == "__main__":
    test_all()
