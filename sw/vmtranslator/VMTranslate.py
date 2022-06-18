#!/usr/bin/env python3
import sys
import os
import click
from Code import *
from Parser import *
#from SymbolTable import *


class VMTranslate:
    def __init__(self, vm, nasm):
        self.vm = vm
        self.nasm = nasm
        self.isFolder = False if os.path.isfile(vm) else True
        self.files = []

    def parseNameToNasm(self, vmFile):
        return vmFile.split(".vm")[0] + ".nasm"

    def getFiles(self):
        if self.isFolder:
            pass
        else:
            conf = {'vm': self.vm}
            self.files.append(conf)
            print(self.files)

    def translate(self):
        code = Code(self.nasm)
        for f in self.files:
            with open(f['vm']) as vmFile:
                parser = Parser(vmFile)
                code.updateVmFileName(f['vm'])
                while parser.advance():
                    current = parser.getCurrent()
                    if current['type'] == 'C_ARITHMETIC':
                        code.writeArithmetic(current['command'])

    def run(self):
        self.getFiles()
        self.translate()
        pass


def testVM():
    f = open('test.nasm', 'w')
    a = VMTranslate('tests/SimpleAdd.vm', f)
    a.run()


@click.command()
@click.argument("vm")
@click.argument("nasm", type=click.File("w"))
def main(vm, nasm):
    # VM can be file ou
    v = VMTranslate(vm, nasm)
    v.run()



if __name__ == "__main__":
    main()
