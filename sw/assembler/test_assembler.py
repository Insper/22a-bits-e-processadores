#!/usr/bin/env python3

import os
import sys
import click
from assembler import *


def compileAll(nasm, hack):
    i = 0
    erro = 0
    print(" 1/2 Removendo arquivos antigos .hack")
    print("  - {}".format(hack))
    clearbin(hack)

    print(" 2/2 Gerando novos arquivos   .hack")
    for n in nasm:
        print("  - {}".format(n))
        e, l = assemblerAll(jar, n, hack, True)
        erro += e
    return e, l


def clearbin(hack):
    try:
        shutil.rmtree(hack)
    except:
        pass


def assemblerAll(nasm, hack):

    error = -1
    log = []

    pwd = os.path.dirname(os.path.abspath(__file__))

    # global path
    os.path.abspath(nasm)
    os.path.abspath(hack)

    if not os.path.exists(os.path.dirname(hack)):
        os.makedirs(os.path.dirname(hack))

    if os.path.isdir(nasm):
        if os.path.isdir(hack):
            for filename in os.listdir(nasm):
                status = "true"
                if filename.strip().find(".nasm") > 0:
                    nHack = hack + filename[:-5] + ".hack"
                    nNasm = nasm + filename
                    fhack = open(nHack, "w")
                    fnasm = open(nNasm, "r")
                    if not os.path.basename(nNasm).startswith("."):
                        print(nNasm)
                        assembler = Assembler(fnasm, fhack)
        #                        log.append(l)
        else:
            logError("output must be folder")


@click.command()
@click.argument("nasmPath")
@click.argument("hackPath")
def main(nasmpath, hackpath):

    i = 0
    erro = 0
    print(" 1/2 Removendo arquivos antigos .hack")
    print("  - {}".format(hackpath))
    clearbin(hackpath)

    print(" 2/2 Gerando novos arquivos   .hack")
    print("  - {}".format(nasmpath))
    assemblerAll(nasmpath, hackpath)
    #      erro += e


# return e, l


if __name__ == "__main__":
    main()
