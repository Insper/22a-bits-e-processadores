#!/usr/bin/env python3
import io
import os
import queue
import uuid


class Code:
    def __init__(self, outFile):
        self.outFile = outFile
        self.counter = 0
        self.vmFileName = None
        self.labelCounter = 0
        self.callLifo = queue.LifoQueue()
        self.mapSegment = {'local': '$LCL', 'argument': '$ARG',
                           'this': '$THIS', 'that': '$THAT'}

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

    def writeInit(self, bootstrap, isDir):
        commands = []

        if bootstrap or isDir:
            commands.append("; Inicialização para VM")

        if bootstrap:
            commands.append("leaw $256,%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw %D,(%A)")

        if isDir:
            commands.append("leaw $Main.main, %A")
            commands.append("jmp")
            commands.append("nop")

        if bootstrap or isDir:
            self.commandsToFile(commands)

    def writeLabel(self, label):
        commands = []
        commands.append('; Label')
        # add function name
        commands.append(self.vmFileName + "." + label + ":")
        self.commandsToFile(commands)

    def writeGoto(self, label):
        commands = []
        commands.append("; Goto Incondicional")
        # add function name
        commands.append("leaw $" + self.vmFileName + "." + label + ",%A")
        commands.append("jmp")
        commands.append("nop")
        self.commandsToFile(commands)

    def writeIf(self, label):
        commands = []
        commands.append("; IF")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("decw %D")
        commands.append("movw %D,(%A)")
        commands.append("movw (%A),%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $" + self.vmFileName + "." + label + ",%A")
        commands.append("jne %D")
        commands.append("nop")
        self.commandsToFile(commands)

    def writeArithmetic(self, command):
        commands = []
        if len(command) < 2:
            print("instrucão invalida {}".format(command))

        self.updateUniqLabel()
        commands.append(self.writeHead(command))

        if command in ["add", 'sub', 'or', 'and']:
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("subw (%A),$1,%A")
            if command == 'add':
                commands.append("addw (%A),%D,%D")
            elif command == 'sub':
                commands.append("subw (%A),%D,%D")
            elif command == 'or':
                commands.append("orw (%A),%D,%D")
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

    def writePop(self, command, segment, index):
        commands = []
        commands.append(self.writeHead(command + ' ' + segment + ' ' + str(index)))
        if segment == "" or segment == "constant":
            return False

        if segment in ['local', 'argument', 'this', 'that']:
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("leaw $" + str(index) + ",%A")
            commands.append("movw %A,%D")
            commands.append("leaw " + self.mapSegment[segment] + ",%A")
            commands.append("addw (%A),%D,%D")
            commands.append("leaw $R15,%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $R15,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
        elif segment == 'temp':
            idx = 5 + 12
            if idx > 12:
                return False
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $" + str(idx) + ",%A")
            commands.append("movw %D,(%A)")
        elif segment == 'static':
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $" + self.vmFileName + "." + str(index) + ",%A")
            commands.append("movw %D,(%A)")
        elif segment == 'pointer':
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("decw %D")
            commands.append("movw %D,(%A)")
            commands.append("movw (%A),%A")
            commands.append("movw (%A),%D")
            if index == 0:
                commands.append("leaw $THIS,%A")
            else:
                commands.append("leaw $THAT,%A")
            commands.append("movw %D,(%A)")

        self.commandsToFile(commands)

    def writePush(self, command, segment, index):
        commands = []
        commands.append(self.writeHead(command + ' ' + segment + ' ' + str(index)))

        if segment == "constant":
            commands.append("leaw $" + str(index) + ",%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")
        elif segment in ['local', 'argument', 'this', 'that']:
            commands.append("leaw $" + str(index) + ",%A")
            commands.append("movw %A,%D")
            commands.append("leaw " + self.mapSegment[segment] + ",%A")
            commands.append("addw (%A),%D,%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")
        elif segment == 'static':
            commands.append("leaw $" + self.vmFileName + "." + str(index) + ",%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")
        elif segment == 'temp':
            idx = index + 5
            if idx > 12:
                return False
            commands.append("leaw $" + str(idx) + ",%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")
        elif segment == 'pointer':
            if index == 0:
                commands.append("leaw $THIS,%A")
            else:
                commands.append("leaw $THAT,%A")
            commands.append("movw (%A),%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")

        self.commandsToFile(commands)

    def writeCall(self, funcName, numArgs):
        commands = []
        commands.append("; chamada de funcao: " + funcName)
        returnLabel = funcName + "-ret-" + str(uuid.uuid4().fields[-1])[0:8]
        self.callLifo.put(returnLabel)

        # return-address
        commands.append("leaw $" + returnLabel + ",%A")
        commands.append("movw %A,%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("incw %D")
        commands.append("movw %D,(%A)")

        # push LCL
        commands.append("leaw $LCL,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("incw %D")
        commands.append("movw %D,(%A)")

        # push ARG
        commands.append("leaw $ARG,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("incw %D")
        commands.append("movw %D,(%A)")

        # push THIS
        commands.append("leaw $THIS,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("incw %D")
        commands.append("movw %D,(%A)")

        # push THAT
        commands.append("leaw $THAT,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("incw %D")
        commands.append("movw %D,(%A)")

        # ARG = SP-n-5
        commands.append("leaw $" + str(numArgs + 5) + ",%A")
        commands.append("movw %A,%D")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%A")
        commands.append("subw %A,%D,%D")
        commands.append("leaw $ARG,%A")
        commands.append("movw %D,(%A)")

        # LCL = SP
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $LCL,%A")
        commands.append("movw %D,(%A)")

        # goto f
        commands.append("leaw $" + funcName + ",%A")
        commands.append("jmp")
        commands.append("nop")

        # ret address
        commands.append(returnLabel + ":")

        self.commandsToFile(commands)

    def writeReturn(self):
        commands = []

        commands.append("; Retorno de função ")

        # FRAME = LCL
        commands.append("leaw $LCL,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $R13,%A") # guarda FRAME
        commands.append("movw %D,(%A)")

        # RET = *(FRAME-5)
        commands.append("leaw $5,%A")
        commands.append("subw %D,%A,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $R14,%A") # guarda RET
        commands.append("movw %D,(%A)")

        #*ARG = pop()
        commands.append("leaw $ARG,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $R15,%A")
        commands.append("movw %D,(%A)")
        commands.append("leaw $SP,%A")
        commands.append("movw (%A),%D")
        commands.append("decw %D")
        commands.append("movw %D,(%A)")
        commands.append("movw %D,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $R15,%A")
        commands.append("movw (%A),%A")
        commands.append("movw %D,(%A)")

        # SP = ARG+1
        commands.append("leaw $ARG,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $SP,%A")
        commands.append("addw %D,$1,(%A)")

        # THAT = *(FRAME-1)
        commands.append("leaw $R13,%A")
        commands.append("subw (%A),$1,%D")
        commands.append("movw %D,(%A)") # faz FRAME--
        commands.append("movw %D,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $THAT,%A")
        commands.append("movw %D,(%A)")

        # THIS = *(FRAME-2)
        commands.append("leaw $R13,%A")
        commands.append("subw (%A),$1,%D")
        commands.append("movw %D,(%A)") # faz FRAME--
        commands.append("movw %D,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $THIS,%A")
        commands.append("movw %D,(%A)")

        # ARG = *(FRAME-3)
        commands.append("leaw $R13,%A")
        commands.append("subw (%A),$1,%D")
        commands.append("movw %D,(%A)") # faz FRAME--
        commands.append("movw %D,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $ARG,%A")
        commands.append("movw %D,(%A)")

        # LCL = *(FRAME-4)
        commands.append("leaw $R13,%A")
        commands.append("subw (%A),$1,%D")
        commands.append("movw %D,(%A)") # faz FRAME--
        commands.append("movw %D,%A")
        commands.append("movw (%A),%D")
        commands.append("leaw $LCL,%A")
        commands.append("movw %D,(%A)")

        # goto RET
        commands.append("leaw $R14,%A")
        commands.append("movw (%A),%A")
        commands.append("jmp")
        commands.append("nop")

        self.commandsToFile(commands)

    def writeFunction(self, funcName, numLocals):
        commands = []
        commands.append(funcName + ":")

        # repeat k times:
        for i in range(numLocals):
            # PUSH 0
            commands.append("leaw $0,%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%A")
            commands.append("movw %D,(%A)")
            commands.append("leaw $SP,%A")
            commands.append("movw (%A),%D")
            commands.append("incw %D")
            commands.append("movw %D,(%A)")

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
    c.writeArithmetic('append')
    commands = f.getvalue().split('\n')
    for idx, command in enumerate(commands[1:]):
        if len(command) > 2:
            assert command == addTestVector[idx]

