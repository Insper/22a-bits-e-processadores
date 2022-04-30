#!/usr/bin/env python3

import yaml
from os import path, listdir
from myhdl import *
from cpu import *
from sequencial import *


def rom_init_from_hack(fileName):
    with open(fileName) as f:
        return [int(l, 2) for l in f.read().splitlines()]


def ram_init_from_mif(mem, fileName):
    init = False
    with open(fileName) as f:
        for l in f.read().splitlines():
            if l.find("END") > -1:
                init = False
            if init:
                v = l.replace(";", ":").split(":")
                address = int(v[0])
                value = int(v[1], 2)
                mem[address] = Signal(value)
            if l.find("BEGIN") > -1:
                init = True


def ram_dump_file(mem, outFile):

    with open(outFile, "w") as f:
        for idx, x in enumerate(mem):
            f.write(str(idx) + " : " + bin(x, 16) + "\n")
        f.close()


def ram_test(mem, testFile):
    cntErro = 0
    with open(testFile, "r") as f:
        for l in f.read().splitlines():
            if len(l.strip()):
                addrBin, valueBin = l.split(":")
                addr = int(addrBin)
                value = int(valueBin, 2)
                valueMem = int(mem[int(addr)])
                if valueMem != value:
                    cntErro = cntErro + 1
                    print("%s: %s | %s" % (addr, bin(value, 16), bin(valueMem, 16)))
        return cntErro
    return -1


@block
def rom_sim(dout, addr, clk, hackFile, width=16, depth=128):

    rom = rom_init_from_hack(hackFile)

    @always(clk.posedge)
    def access():
        address = int(addr)
        if address >= len(rom):
            dout.next = 0x20000
        else:
            dout.next = rom[address]

    return instances()


def ram_clear(mem, depth):
    mem = [Signal(intbv(0)) for i in mem]


@block
def ram_sim(mem, dout, din, addr, we, clk, mifFile, width=16, depth=128, dump=True):
    ram_init_from_mif(mem, mifFile)

    @always(clk.posedge)
    def logic():
        if we:
            mem[addr.val].next = din
        dout.next = mem[addr.val]

    return instances()


# TODO: Edu consegue debugar isso e entender pq não funciona?
# com o dicionário, ele muda o valor do nada na execucao
# com dic seria bem melhor, pq conseuguimos exportar somente
# o que foi alterado, e ocupamos muito menos memória
@block
def ram_sim2(dout, din, addr, we, clk, mifFile, width=16, depth=128):
    memory = {}
    ram_init_from_mif(memory, mifFile)
    print("----init ")

    @always(clk.posedge)
    def access():
        if we:
            memory[int(addr.val)] = din.val
        else:
            if int(addr.val) in memory.keys():
                dout.next = memory[int(addr.val)]
            else:
                dout.next = 0

    return access


@block
def test_cpu(mem, inRamMif, inRomHack, lst_data):
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = Signal(bool(0))

    cpu_1 = cpu(
        inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, lst_data
    )
    ram_1 = ram_sim(
        mem, inMem, outMem, addressM, writeM, clkMem, inRamMif, depth=2**15 - 1
    )
    rom_1 = rom_sim(instruction, pcount, clk, inRomHack)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(delay(5))
    def clkgenMem():
        clkMem.next = not clkMem

    @instance
    def rst():
        rst.next = 1
        yield delay(5)
        rst.next = 0

    return instances()


def lstHeader():
    h = []
    h.append("ps")
    h.append("clock")
    h.append("instruction")
    h.append("pcout")
    h.append("s_regDout")
    h.append("s_regSout")
    h.append("s_regAout")
    h.append("c_muxALUI_A")
    h.append("c_muxSD_ALU")
    h.append("outM")
    h.append("writeM")
    h.append("inM")
    return h


def lstWrite(lstFile, data, lstHeader):
    f = open(lstFile, "w")
    f.write(tabulate(data, headers=lstHeader, tablefmt="plain"))
    f.close()


def run_cpu_test(name, inRamMif, inRomHack, testFile, time):
    print("--- %s ---" % name)
    mem = [Signal(intbv(0)) for i in range(2**15 - 1)]
    lst_data = []
    tb = test_cpu(mem, inRamMif, inRomHack, lst_data)
    tb.config_sim(trace=True, tracebackup=False)
    tb.run_sim(time)
    ram_dump_file(mem, path.join("tstAssembly", name + "_ram_dump.txt"))
    if ram_test(mem, testFile) == 0:
        print("ok")

    breakpoint()
    lstWrite("SIM.lst", lst_data, lstHeader())
    tb.quit_sim()
    mem = []


class cpuTest:
    def __init__(self, folderPath):
        self.confFileName = "config.yml"
        self.folderPath = folderPath
        self.tests = []
        self.readTestsFromConf()

        for i in self.tests:
            self.getTestFilesFromTestName(i)

    def readTestsFromConf(self):
        try:
            with open(path.join(self.folderPath, self.confFileName), "r") as file:
                conf = yaml.load(file, Loader=yaml.FullLoader)
                self.tests = conf["test_files"]
                return
        except FileNotFoundError:
            print("%s: file not found" % self.confFileName)
            return False

    def getTestFilesFromTestName(self, name):
        romFile = path.join(self.folderPath, "hack", name + ".hack")
        if path.exists(romFile) == False:
            print("%s: file not found" % romFile)
            return False

        tstFolder = path.join(self.folderPath, "tests", name + "/")
        if path.exists(romFile) == False:
            print("%s: dir not found" % tstFolder)
            return False

        tests = []
        for file in listdir(tstFolder):
            if "_in.mif" in file:
                tstName = file[:-7]
                mif = path.join(tstFolder, file)
                tst = path.join(tstFolder, tstName + "_tst.mif")
                tests.append(
                    {
                        "name": tstName,
                        "romFile": romFile,
                        "ramFile": mif,
                        "tstFile": tst,
                    }
                )

        for t in tests:
            run_cpu_test(
                t["name"],
                t["ramFile"],
                t["romFile"],
                t["tstFile"],
                10000,
            )


if __name__ == "__main__":
    print("---- cpu ----")
    test = cpuTest("tstAssembly")
    # run_cpu_test(
    #    "add0",
    #    "tstAssembly/tests/add/add0_in.mif",
    #    "tstAssembly/hack/add.hack",
    #    "tstAssembly/tests/add/add0_tst.mif",
    #    300,
    # )
    #
