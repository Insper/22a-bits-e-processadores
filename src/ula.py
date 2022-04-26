#!/usr/bin/env python3

from myhdl import block, always_comb, Signal, intbv, modbv, instances, ConcatSignal, bin


@block
def ula(x, y, c, zr, ng, saida):

    zx_out = Signal(intbv(0))
    nx_out = Signal(intbv(0))
    zy_out = Signal(intbv(0))
    ny_out = Signal(intbv(0))
    and_out = Signal(intbv(0))
    add_out = Signal(intbv(0))
    mux_out = Signal(intbv(0))
    no_out = Signal(intbv(0))

    c_zx = c(5)
    c_nx = c(4)
    c_zy = c(3)
    c_ny = c(2)
    c_f = c(1)
    c_no = c(0)

    zx = zerador(c_zx, x, zx_out)
    nx = inversor(c_nx, zx_out, nx_out)

    zy = zerador(c_zy, y, zy_out)
    ny = inversor(c_ny, zy_out, ny_out)

    add = add16(nx_out, ny_out, add_out)

    no = inversor(c_no, mux_out, no_out)
    comp = comparador(no_out, zr, ng)

    @always_comb
    def comb():
        if c_f == 1:
            mux_out.next = add_out
        else:
            mux_out.next = nx_out & ny_out

        saida.next = no_out[len(saida) :]

    return instances()


# -z faz complemento de dois
# ~z inverte bit a bit
@block
def inversor(z, a, y):
    @always_comb
    def comb():
        if z == 1:
            y.next = ~a
        else:
            y.next = a

    return comb


@block
def comparador(a, zr, ng):
    @always_comb
    def comb():
        ng.next = 0
        zr.next = 0
        if a < 0:
            ng.next = 1
            zr.next = 0
        if a == 0:
            zr.next = 1
            ng.next = 0

    return comb


@block
def zerador(z, a, y):
    @always_comb
    def comb():
        if z == 1:
            y.next = 0
        else:
            y.next = a

    return comb


@block
def add(a, b, q):
    @always_comb
    def comb():
        q.next = a + b

    return comb


@block
def inc16(a, q):
    one = Signal(intbv(1))

    add16_1 = add16(a, one, q)

    return add16_1


@block
def add16(a, b, q, n=16):
    # nao podemos acessar direto um intbv como
    # se fosse um sinal. Devemos criar um shadow signal
    # que eh apenas readonly!
    _a = [a(i) for i in range(n)]
    _b = [b(i) for i in range(n)]
    _c = [Signal(bool(0)) for i in range(n + 1)]
    _q = [Signal(bool(0)) for i in range(n)]

    out_q = ConcatSignal(*reversed(_q))

    fa_list = [None for i in range(n)]
    for i in range(len(fa_list)):
        fa_list[i] = fullAdder(_a[i], _b[i], _c[i], _q[i], _c[i + 1])

    @always_comb
    def comb():
        q.next = out_q

    return instances()


@block
def fullAdder(a, b, c, q, carry):
    s1 = Signal(bool(0))
    s2 = Signal(bool(0))
    s3 = Signal(bool(0))

    half_1 = halfAdder(a, b, s1, s2)
    half_2 = halfAdder(c, s1, q, s3)

    @always_comb
    def comb():
        carry.next = s2 | s3

    return instances()


@block
def halfAdder(a, b, q, carry):
    @always_comb
    def comb():
        carry.next = a & b
        q.next = a ^ b

    return comb
