#!/usr/bin/env python3

import os
import sys
import click
from assembler import *


def clearbin(hackPath):
    try:
        shutil.rmtree(hackPath)
    except:
        pass


def assemblerFromDir(nasmPath, hackPath):
    nasmPath = os.path.abspath(nasmPath)
    hackPath = os.path.abspath(hackPath)

    print(" 1/2 Removendo arquivos antigos .hackPath")
    print("  - {}".format(hackPath))
    clearbin(hackPath)

    print(" 2/2 Gerando novos arquivos .hackPath")
    print(" Destine: {}".format(hackPath))

    if os.path.exists(hackPath) == False:
        os.makedirs(hackPath)

    if os.path.isdir(nasmPath) and os.path.isdir(hackPath):
        for filename in os.listdir(nasmPath):
            if filename.strip().find(".nasm") > 0:
                nHack = os.path.join(hackPath, filename[:-5] + ".hack")
                nNasm = os.path.join(nasmPath, filename)
                fhack = open(nHack, "w")
                fnasm = open(nNasm, "r")
                if not os.path.basename(nNasm).startswith("."):
                    print("\t" + filename[:-5] + ".hack")
                    assembler = Assembler(fnasm, fhack)
    else:
        print("output must be folder")


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


if __name__ == "__main__":
    main()
