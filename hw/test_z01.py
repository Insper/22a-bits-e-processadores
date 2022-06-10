#!/usr/bin/env python3

from myhdl import *
from cpu import *
from sequencial import *
from hw_util import *

import os.path


@block
def z01_sim(mem, inRomHack, lst_data):
    instruction = Signal(intbv(0)[18:])
    inMem, outMem = [Signal(intbv(15)[16:]) for i in range(2)]
    pcount, addressM = [Signal(intbv(0)[15:]) for i in range(2)]
    writeM, clk = [Signal(bool(0)) for i in range(2)]
    clkMem = Signal(bool(0))
    rst = ResetSignal(0, active=1, isasync=True)

    cpu_1 = cpu(
        inMem, instruction, outMem, addressM, writeM, pcount, rst, clk, lst_data
    )
    ram_1 = ram_sim(mem, inMem, outMem, addressM, writeM, clkMem, depth=2**15 - 1)
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


class test_z01:
    def __init__(self):
        self.config = ""
        self.testsConfig = []
        self.mem = []
        self.lst_data = []

    def updateConfig(self, config):
        self.lst_data = []
        self.mem = []
        self.config = config

    def baseAddress(self, folder, name):
        return path.join(folder, name)

    def getTestFilesFromTestName(self, tstFolder):
        for file in listdir(tstFolder):
            if "_in.mif" in file:
                name = file[:-7]
                mif = path.join(tstFolder, file)
                tst = path.join(tstFolder, name + "_tst.mif")
                basePath = os.path.join(tstFolder, name) + "{}"
                refMem = basePath.format("_tst.mif")
                dumpMem = basePath.format("_ram_dump.txt")
                inMem = basePath.format("_in.mif")
                trace = basePath.format("")
                self.testsConfig.append(
                    {
                        "tstFolder": tstFolder,
                        "name": name,
                        "ramFile": mif,
                        "tstFile": tst,
                        "basePath": basePath,
                        "refMem": refMem,
                        "dumpMem": dumpMem,
                        "inMem": inMem,
                        "trace": trace,
                    }
                )
        return self.testsConfig

    def run(self):
        print("--- %s ---" % self.config["name"])
        self.mem = ram_init_from_mif(self.config["inMem"])
        tb = z01_sim(self.mem, self.config["romFile"], self.lst_data)
        tb.config_sim(trace=True, name=self.config["trace"], tracebackup=False)
        tb.run_sim(self.config["runTime"])
        tb.quit_sim()

    def dump(self):
        mem_dump_file(self.mem, self.config["dumpMem"])
        lstWrite(self.lst_data, self.config["trace"])

    def test(self, ref, dut):
        if ram_test(ref, dut) == 0:
            return 0
        else:
            return 1
