#!/usr/bin/env python3
import sys
import os
import click


class Parser:
    def __init__(self, inputFile):
        self.currentLine = None
        self.currentCommand = None
        self.currentArg0 = None
        self.currentArg1 = None
        self.file = inputFile

    def advance(self):
        while True:
            line = self.file.readline()
            if not line:
                self.currentLine = None
                self.currentType = None
                self.currentCommand = None
                self.currentArg0 = None
                self.currentArg1 = None
                return False
            self.currentLine = line
            line = line.split("//")[0].rstrip()
            if line.strip():
                self.currentLine = line.replace(",", " ").split()
                self.currentCommand = self.command()
                self.currentArg0 = self.arg0()
                self.currentArg1 = self.arg1()
                self.currentType = self.commandType()
                return True

    def getCurrent(self):
        return {'type': self.currentType,
                'command': self.currentCommand,
                'arg0': self.currentArg0,
                'arg1': self.currentArg1}

    def command(self, line=None):
        if line is None:
            line = self.currentLine
        return line[0]

    def arg0(self, line=None):
        if line is None:
            line = self.currentLine
        if len(line) > 1:
            return line[1]
        else:
            return None

    def arg1(self, line=None):
        if line is None:
            line = self.currentLine
        if len(line) > 2:
            return int(line[2])
        else:
            return None

    def commandType(self, command=None):
        if command is None:
            command = self.currentCommand
        if command == "push":
            return "C_PUSH"
        elif command == "pop":
            return "C_POP"
        elif command == "label":
            return "C_LABEL"
        elif command == "goto":
            return "C_GOTO"
        elif command == "if-goto":
            return "C_IF"
        elif command == "function":
            return "C_FUNCTION"
        elif command == "return":
            return "C_RETURN"
        elif command == "call":
            return "C_CALL"
        else:
            return "C_ARITHMETIC"

    def close(self):
        self.file.close()


def test_advance():
    with open("tests/SimplePushAdd.vm") as file:
        p = Parser(file)
        assert p.advance()
        assert p.currentLine == ["push", "constant", "5"]
        assert p.advance()
        assert p.currentLine == ["push", "constant", "9"]
        assert p.advance()
        assert p.currentLine == ["add"]
        assert not p.advance()
        p.close()


def test_command():
    p = Parser('')
    assert p.command(["push", "constant", "5"]) == "push"
    assert p.command(["add"]) == "add"
    assert p.command(["label", "bata"]) == "label"


def test_commandType():
    p = Parser('')
    assert p.commandType("push") == "C_PUSH"
    assert p.commandType("add") == "C_ARITHMETIC"
    assert p.commandType("label") == "C_LABEL"


def test_args():
    p = Parser('')
    assert p.arg0(["push", "constant", "5"]) == "constant"
    assert p.arg1(["push", "constant", "5"]) == 5


if __name__ == "__main__":
    test_advance()
