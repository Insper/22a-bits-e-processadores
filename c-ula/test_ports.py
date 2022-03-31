#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from modulos import (
    fullAdder,
    halfAdder,
    add16,
    zerador,
    inc16,
    comparador,
    inversor,
    ula,
)

random.seed(5)
randrange = random.randrange


def convert_add16(hdl):
    q, a, b = [Signal(intbv(0)[15:0]) for i in range(3)]
    add_1 = add16(a, b, q, 16)
    add_1.convert(hdl=hdl)


@block
def test_ula():
    x = Signal(intbv(1)[16:])
    y = Signal(intbv(2)[16:])
    saida = Signal(intbv(0)[16:])
    control = Signal(intbv(0))
    zr = Signal(bool(0))
    ng = Signal(bool(0))
    ula_1 = ula(x, y, control, zr, ng, saida)

    @instance
    def stimulus():
        control.next = 0b000010
        yield delay(10)
        if saida != x + y:
            print("erro")

        control.next = 0b000000
        yield delay(10)
        if saida != x and y:
            print("erro")

        control.next = 0b100010
        yield delay(10)
        if saida != y:
            print("erro")

        control.next = 0b001010
        yield delay(10)
        if saida != x:
            print("erro")

        control.next = 0b100110
        yield delay(10)
        if saida != ~y:
            print("erro")

        control.next = 0b011010
        yield delay(10)
        if saida != ~x:
            print("erro")

        control.next = 0b101010
        yield delay(10)
        if saida != 0:
            print("erro")

        control.next = 0b101000
        yield delay(10)
        if saida != 0:
            print("erro")

        control.next = 0b101001
        yield delay(10)
        if saida != intbv(-1)[16:]:
            print("erro")

        # ------ zr ng --------#
        if zr != 0 and ng != 1:
            print("erro")

        control.next = 0b101000
        yield delay(10)
        if zr != 1 and ng != 0:
            print("erro")

        control.next = 0b000010
        yield delay(10)
        if zr != 0 and ng != 0:
            print("erro")

    return ula_1, stimulus


@block
def test_zerador():
    z = Signal(bool(0))
    a = Signal(intbv(0))
    y = Signal(intbv(0))
    zerador_1 = zerador(z, a, y)

    @instance
    def stimulus():
        a.next = randrange(2**16 - 1)
        z.next = 0
        yield delay(10)
        if y != a:
            print("erro 1")
            print("%s %s %s" % (bin(z, 1), bin(a, 16), bin(y, 16)))
        z.next = 1
        yield delay(10)
        if y != 0:
            print("erro 2")
            print("%s %s %s" % (bin(z, 1), bin(a, 16), bin(y, 16)))

    return zerador_1, stimulus


@block
def test_comparador():
    a = Signal(intbv(0))
    ng = Signal(bool(0))
    zr = Signal(bool(0))
    comparador_1 = comparador(a, zr, ng)

    @instance
    def stimulus():
        a.next = 0
        yield delay(10)
        if ng != 0 or zr != 1:
            print("erro 1")
            print("%s %s %s" % (bin(a, 16), bin(zr, 1), bin(ng, 1)))
        a.next = -1
        yield delay(10)
        if ng != 1 or zr != 0:
            print("erro 2")
            print("%s %s %s" % (bin(a, 16), bin(zr, 1), bin(ng, 1)))
        a.next = 32
        yield delay(10)
        if ng != 0 or zr != 0:
            print("erro 3")
            print("%s %s %s" % (bin(a, 16), bin(zr, 1), bin(ng, 1)))

    return comparador_1, stimulus


@block
def test_inversor():
    z = Signal(bool(0))
    a = Signal(intbv(0))
    y = Signal(intbv(0))

    inversor_1 = inversor(z, a, y)

    @instance
    def stimulus():
        for i in range(256):
            a.next = randrange(2**16 - 1)
            z.next = randrange(2)
            yield delay(10)
            if z == 0:
                if a != y:
                    print("erro")
                    print("%s %s %s" % (bin(z, 1), bin(a, 16), bin(y, 16)))
                    break
            else:
                if a != ~y:
                    print("erro")
                    print("%s %s %s" % (bin(z, 1), bin(a, 16), bin(y, 16)))
                    break

    return inversor_1, stimulus


@block
def test_inc16():
    a = Signal(intbv(0))
    q = Signal(intbv(0))

    inc16_1 = inc16(a, q)

    @instance
    def stimulus():
        for i in range(256):
            a.next = randrange(2**16 - 2)
            yield delay(1)
            if q != a + 1:
                print("erro")
                print("%s %s" % (a, q))
                print("%s %s" % (bin(a, 16), bin(q, 16)))
                break

    return inc16_1, stimulus


@block
def test_add16():
    a = Signal(intbv(0))
    b = Signal(intbv(0))
    q = Signal(intbv(0))

    add16_1 = add16(a, b, q)

    @instance
    def stimulus():
        for i in range(256):
            a.next, b.next = [randrange(2**15 - 1) for i in range(2)]
            yield delay(1)
            if q != a + b:
                print("erro")
                print("%s %s %s" % (a, b, q))
                print("%s %s %s" % (bin(a, 16), bin(b, 16), bin(q, 16)))
                print("%s" % (bin(a + b, 16)))
                break

    return add16_1, stimulus


@block
def test_fullAdder():
    a = Signal(bool(0))
    b = Signal(bool(0))
    c = Signal(bool(0))
    q = Signal(bool(0))
    carry = Signal(bool(0))

    testTable = [
        [0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]

    fullAdder_1 = fullAdder(a, b, c, q, carry)

    @instance
    def stimulus():
        erroCnt = 0
        for n in testTable:
            a.next = n[0]
            b.next = n[1]
            c.next = n[2]
            yield delay(10)
            if q != n[3] or carry != n[4]:
                erroCnt = erroCnt + 1
                print(n)
                print("q: %s / carry: %s" % (q, carry))

    return fullAdder_1, stimulus


if __name__ == "__main__":
    print("---- fullAdder----")
    tb = test_fullAdder()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- add16 ----")
    tb = test_add16()
    # tb.config_sim(trace=True)
    tb.run_sim()
    # convert_add16(hdl="vhdl")

    print("---- inc16 ----")
    tb = test_inc16()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- zerador ----")
    tb = test_zerador()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- comparador ----")
    tb = test_comparador()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- inversor ----")
    tb = test_inversor()
    # tb.config_sim(trace=True)
    tb.run_sim()

    print("---- ula ----")
    tb = test_ula()
    tb.run_sim()
