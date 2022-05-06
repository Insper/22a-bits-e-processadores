import sys
import click
from SymbolTable import *
from Code import *
from Parser import *


class Assembler:
    def __init__(self, nasm, hack):
        self.hack = hack
        self.symbolTable = SymbolTable()
        self.parser = Parser(nasm)
        self.code = Code()
        self.fillSymbolTable()
        self.generateMachineCode()

    def fillSymbolTable(self):

        # label
        rom = 0
        while self.parser.advanced():
            if self.parser.commandType() == "L_COMMAND":
                l = self.parser.label()
                if self.symbolTable.contains(l):
                    raise Exception("Label ja declarado: {}".format(l))
                self.symbolTable.addEntry(l, rom)
            else:
                rom = rom + 1
        self.parser.reset()

        # leaw $MEM
        # talvez tirar isso aqui da entrega do assembler
        # e colocar no vmtranslator
        ram = 16
        while self.parser.advanced():
            if self.parser.commandType() == "A_COMMAND":
                name = self.parser.symbol()
                if not name.isdigit():
                    if not self.symbolTable.contains(name):
                        self.symbolTable.addEntry(name, ram)
                        ram = ram + 1
        self.parser.reset()
        # print(self.symbolTable.table)

    def generateMachineCode(self):
        while self.parser.advanced():
            if self.parser.commandType() == "C_COMMAND":
                c = self.parser.command()
                bin = (
                    "1"
                    + "000"
                    + self.code.comp(c)
                    + "0"
                    + self.code.dest(c)
                    + self.code.jump(c)
                )
                print(len(bin))
                self.hack.write(bin + "\n")
                # print(c); print(bin)
            elif self.parser.commandType() == "A_COMMAND":
                l = self.parser.symbol()
                if self.symbolTable.contains(l):
                    l = self.code.toBinary(self.symbolTable.getAddress(l))
                bin = "0" + "0" + self.code.toBinary(l)
                print(len(bin))
                self.hack.write(bin + "\n")
        pass


@click.command()
@click.argument("nasm", type=click.File("r"))
@click.argument("hack", type=click.File("w"))
def main(nasm, hack):
    assembler = Assembler(nasm, hack)


if __name__ == "__main__":
    main()
