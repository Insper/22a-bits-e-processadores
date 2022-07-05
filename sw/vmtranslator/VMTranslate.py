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
        self.bootstrap = False

    def enableBootstrap(self):
        self.bootstrap = True

    def parseNameToNasm(self, vmFile):
        return vmFile.split(".vm")[0] + ".nasm"

    def getFiles(self):
        self.files = []
        if self.isFolder:
            for file in os.listdir(self.vm):
                if file[-2:] == 'vm':
                    self.files.append(os.path.join(self.vm, file))
        else:
            self.files.append(self.vm)
        print(self.files)

    def translate(self):
        code = Code(self.nasm)
        code.writeInit(self.bootstrap, self.isFolder)
        for f in self.files:
            with open(f) as vmFile:
                parser = Parser(vmFile)
                code.updateVmFileName(f)
                while parser.advance():
                    current = parser.getCurrent()
                    if current['type'] == 'C_ARITHMETIC':
                        code.writeArithmetic(current['command'])
                    elif current['type'] == 'C_POP':
                        code.writePop(current['command'],
                                      current['arg0'], current['arg1'])
                    elif current['type'] == 'C_PUSH':
                        code.writePush(current['command'],
                                       current['arg0'], current['arg1'])
                    elif current['type'] == 'C_LABEL':
                        code.writeLabel(current['arg0'])
                    elif current['type'] == 'C_GOTO':
                        code.writeGoto(current['arg0'])
                    elif current['type'] == 'C_IF':
                        code.writeIf(current['arg0'])
                    elif current['type'] == 'C_CALL':
                        code.writeCall(current['arg0'], current['arg1'])
                    elif current['type'] == 'C_RETURN':
                        code.writeReturn()
                    elif current['type'] == 'C_FUNCTION':
                        code.writeFunction(current['arg0'], current['arg1'])

    def run(self):
        self.getFiles()
        self.translate()
        pass

    def close(self):
        self.vm.close()


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
