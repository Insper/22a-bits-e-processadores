#!/usr/bin/env python3
import io
import os


class Code:
    def __init__(self, outFile):
        self.outFile = outFile
        self.counter = 0
        self.vmFileName = None
        self.labelCounter = 0

    def updateVmFileName(self, name):
        self.vmFileName = os.path.basename(name).split('.')[0]

    def commandsToFile(self, commands):
        for line in commands:
            self.outFile.write(f'{line}\n')

    def getUniqLabel(self):
        return self.vmFileName + str(self.labelCounter)

    def updateUniqLabel(self):
        self.labelCounter = self.labelCounter + 1

    def writeHead(self, command):
        self.counter = self.counter + 1
        return(";; " + command + " - " + str(self.counter))

    def writeArithmetic(self, command):
        commands = []
        if len(command) < 2:
            print("instrucão invalida {}".format(command))

        self.updateUniqLabel()
        commands.append(self.writeHead(command))

        if command == "add":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("addw (%A),%D,%D")
            commands.append("movw %D,(%A)")
        elif command == "sub":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("subw (%A),%D,%D")
            commands.append("movw %D,(%A)")
        elif command == "not":
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw (%A),%D")
            commands.append("notw %D")
            commands.append("movw %D,(%A)")
        elif command == "neg":
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw (%A),%D")
            commands.append("negw %D")
            commands.append("movw %D,(%A)")
        elif command == "and":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("andw (%A),%D,%D")
            commands.append("movw %D,(%A)")
        elif command == "or":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("orw (%A),%D,%D")
            commands.append("movw %D,(%A)")
        elif command == "eq":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("subw (%A),%D,%D")
            commands.append("leaw $EQ" + self.getUniqLabel() + ",%A")
            commands.append("je %D")
            commands.append("nop")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $0,(%A)")
            commands.append("leaw $EQ2" + self.getUniqLabel() + ",%A")
            commands.append("jmp")
            commands.append("nop")
            commands.append("EQ" + self.getUniqLabel() + ":")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $-1,(%A)")
            commands.append("EQ2" + self.getUniqLabel() + ":")
        elif command == "gt":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("subw (%A),%D,%D")
            commands.append("leaw $GT" + self.getUniqLabel() + ",%A")
            commands.append("jg %D")
            commands.append("nop")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $0,(%A)")
            commands.append("leaw $GT2" + self.getUniqLabel() + ",%A")
            commands.append("jmp")
            commands.append("nop")
            commands.append("GT" + self.getUniqLabel() + ":")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $-1,(%A)")
            commands.append("GT2" + self.getUniqLabel() + ":")
        elif command == "lt":
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("subw (%A),%D,%D")
            commands.append("leaw $LT" + self.getUniqLabel() + ",%A")
            commands.append("jl %D")
            commands.append("nop")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $0,(%A)")
            commands.append("leaw $LT2" + self.getUniqLabel() + ",%A")
            commands.append("jmp")
            commands.append("nop")
            commands.append("LT" + self.getUniqLabel() + ":")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            commands.append("movw $-1,(%A)")
            commands.append("LT2" + self.getUniqLabel() + ":")

        self.commandsToFile(commands)


addTestVector = [
            "leaw $SP,%A",
            "movw (%A),%D",
            "decw %D",
            "movw %D,(%A)",
            "movw (%A),%A",
            "movw (%A),%D",
            "leaw $SP,%A",
            "subw (%A),$1,%A",
            "addw (%A),%D,%D",
            "movw %D,(%A)",
]


def test_writeArithmetic():
    f = io.StringIO()
    c = Code(f)
    c.writeArithmetic('add')
    commands = f.getvalue().split('\n')
    for idx, command in enumerate(commands[1:]):
        if len(command) > 2:
            assert command == addTestVector[idx]

