#!/usr/bin/env python3
import random
from myhdl import block, instance, Signal, intbv, delay, bin
from modulos import ula
import argparse

random.seed(5)
randrange = random.randrange


def input_wrapper(input_func):
    def wrapper(*args, **kwargs):
        inp = input_func(*args, **kwargs)
        if len(inp) != 6:
            raise ValueError("Input length must be 6")
        elif inp.isalpha():
            raise ValueError("Non 1/0 found")
        return inp

    return wrapper


custom_input = input_wrapper(input)


@block
def run_ula(x, y):
    x = Signal(intbv(x)[16:])
    y = Signal(intbv(y)[16:])
    saida = Signal(intbv(0)[16:])
    control = Signal(intbv(0))
    zr = Signal(bool(0))
    ng = Signal(bool(0))
    ula_1 = ula(x, y, control, zr, ng, saida)

    @instance
    def stimulus():
        print("Escreva o sinal de controle da ula")
        print("exemplo: 100010")
        while True:
            control.next = int(custom_input("zx nx zy ny f no: "), 2)
            yield delay(10)
            print("\t x: %s | y: %s" % (bin(x, 16), bin(y, 16)))
            print("\t saida: %s" % bin(saida, 16))
            print("\t zr %s | ng %s" % (bin(zr, 1), bin(ng, 1)))

    return ula_1, stimulus


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z01 ULA TEST")
    parser.add_argument(
        "--inputs",
        type=int,
        nargs=2,
        help="an integer for the accumulator",
        default=[1, -1],
    )
    args = parser.parse_args()
    x = args.inputs[0]
    y = args.inputs[1]
    print("Executando a ULA com as entradas:")

    tb = run_ula(x, y)
    tb.run_sim()
