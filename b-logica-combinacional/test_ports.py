#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from ports import and16, or8way, orNway, barrelShifter
import pdb

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


if __name__ == "__main__":
    print("---- and16 ----")
    tb = test_and16()
    tb.run_sim()

    print("---- or8way ----")
    tb = test_orNway()
    tb.run_sim()

    print("---- barrelshifter ----")
    tb = test_barrelShifter()
    tb.run_sim()
