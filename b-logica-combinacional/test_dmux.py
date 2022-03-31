#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from dmux import deMux8Way, deMux4Way, deMux2Way

random.seed(5)
randrange = random.randrange


def convert(hdl):
    a, q0, q1, q2, q3, q4 = [Signal(intbv(0)[16:0]) for i in range(6)]
    sel = Signal(intbv(0)[2:0])
    sig = [q0, q1, q2, q3, q4]

    dmux4Way_1 = dmux(a, sig, sel)
    dmux4Way_1.convert(hdl=hdl)


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


if __name__ == "__main__":
    print("---- deMux2Way ----")
    tb = test_deMux2Way()
    tb.run_sim()

    print("---- deMux4Way ----")
    tb = test_deMux4Way()
    tb.run_sim()

    print("---- deMux8Way ----")
    tb = test_deMux8Way()
    tb.run_sim()
