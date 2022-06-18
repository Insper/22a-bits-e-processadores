import sys


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.init()

    def init(self):
        for i in range(0, 17):
            self.table["R" + str(i)] = i

        self.table["KBD"] = 24576
        self.table["SCR"] = 16384
        self.table["SCREEN"] = 16384

        self.table["SP"] = 0
        self.table["LCL"] = 1
        self.table["ARG"] = 2
        self.table["THIS"] = 3
        self.table["THAT"] = 4

    def addEntry(self, symbol: str, address: int):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def getAddress(self, symbol):
        return self.table[symbol]


def test_init():
    s = SymbolTable()

    assert s.table["R5"] == 5
    assert s.table["KBD"] == 24576


def test_addEntry():
    s = SymbolTable()
    s.addEntry("abobrina", 13)
    assert s.table["abobrina"] == 13


def test_contains():
    s = SymbolTable()
    assert s.contains("abobrina") == False
    assert s.contains("R13") == True


def test_getAddress():
    s = SymbolTable()
    assert s.getAddress("R10") == 10


if __name__ == "__main__":
    pass
